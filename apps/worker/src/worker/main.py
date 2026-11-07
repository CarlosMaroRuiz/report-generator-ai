import asyncio
import logging
import signal

from bullmq import Worker

from worker import infra
from worker.config import settings
from worker.handler import process_job

log = logging.getLogger('worker')

async def on_failed(job, err):
    log.warning('job %s agotó reintentos: %s', job.data.get('taskId'), err)

async def on_stalled(job_id: str):
    log.warning('job %s quedó stalled', job_id)

async def main() -> None:
    logging.basicConfig(level=settings.log_level,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    worker = Worker(
        settings.queue_name, process_job,
        {'connection': settings.redis_url, 'prefix': settings.queue_prefix,
         'concurrency': settings.concurrency},
    )
    worker.on('failed', on_failed)
    worker.on('stalled', on_stalled)

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop.set)

    log.info('escuchando %s con concurrencia %d', settings.queue_name, settings.concurrency)
    await stop.wait()

    log.info('señal recibida: terminando jobs en curso')
    try:
        await asyncio.wait_for(worker.close(), timeout=settings.shutdown_timeout)
    except asyncio.TimeoutError:
        log.warning('cierre forzado tras %ds', settings.shutdown_timeout)
        await worker.close(force=True)

    await infra.close()
    log.info('worker detenido')

if __name__ == '__main__':
    asyncio.run(main())