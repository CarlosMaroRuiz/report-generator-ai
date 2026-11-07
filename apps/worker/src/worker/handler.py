import asyncio
import logging
import re
import unicodedata
from datetime import datetime, timezone

import httpx
from bullmq import UnrecoverableError
from pydantic import ValidationError

from worker import infra
from worker.ai import generate
from worker.config import settings
from worker.render import build_html
from worker.schemas import ReportJob

log = logging.getLogger('worker')

def slug(text: str, n: int = 60) -> str:
    s = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()[:n].rstrip('-') or 'reporte'

async def process_job(job, token):
    try:
        data = ReportJob.model_validate(job.data)
    except ValidationError as exc:
        raise UnrecoverableError(f'payload inválido: {exc.errors()[0]["msg"]}')

    tid = data.task_id
    log.info('job %s | %s', tid, data.topic[:80])
    await job.updateProgress(5)

    try:
        await job.updateProgress(15)
        report = await asyncio.wait_for(generate(data), timeout=settings.ai_timeout)

        await job.updateProgress(60)
        meta = {
            'task_id': tid, 'model': settings.ai_model,
            'start_date': data.start_date, 'end_date': data.end_date,
            'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),
        }
        pdf = await infra.to_pdf(build_html(report, meta))
        if not pdf.startswith(b'%PDF'):
            raise RuntimeError('Gotenberg no devolvió un PDF')

        await job.updateProgress(85)
        key = f'exports/{slug(report.title)}-{tid[:8]}.pdf'
        await infra.upload(pdf, key)

        await job.updateProgress(95)
        result = {
            'taskId': tid, 'status': 'completed', 's3Url': infra.presign(key),
            'title': report.title, 'message': 'Reporte generado y almacenado.',
        }
        await infra.emit(result)
        await job.updateProgress(100)
        log.info('job %s completado (%d KB)', tid, len(pdf) // 1024)
        return result

    except asyncio.TimeoutError as exc:
        await infra.emit({'taskId': tid, 'status': 'failed', 'error': 'timeout del modelo'})
        raise TimeoutError(f'el modelo superó {settings.ai_timeout}s') from exc

    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        msg = f'gotenberg {code}'
        await infra.emit({'taskId': tid, 'status': 'failed', 'error': msg})
        if 400 <= code < 500 and code not in (408, 429):
            raise UnrecoverableError(msg) from exc   # no reintentar
        raise

    except Exception as exc:
        msg = f'{type(exc).__name__}: {exc}'
        await infra.emit({'taskId': tid, 'status': 'failed', 'error': msg})
        log.exception('job %s falló', tid)
        raise