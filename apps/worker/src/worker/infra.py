import asyncio
import json

import boto3
import httpx
from redis.asyncio import Redis

from worker.config import settings

_redis = Redis.from_url(settings.redis_url, decode_responses=True)

_s3 = boto3.client(
    's3', endpoint_url=settings.s3_endpoint,
    aws_access_key_id=settings.minio_root_user,
    aws_secret_access_key=settings.minio_root_password,
    region_name='us-east-1')

_s3_public = boto3.client(
    's3', endpoint_url=settings.s3_public_endpoint,
    aws_access_key_id=settings.minio_root_user,
    aws_secret_access_key=settings.minio_root_password,
    region_name='us-east-1')

_gotenberg = httpx.AsyncClient(base_url=settings.gotenberg_url,
                               timeout=settings.gotenberg_timeout)

async def to_pdf(doc_html: str) -> bytes:
    r = await _gotenberg.post(
        '/forms/chromium/convert/html',
        files={'index.html': ('index.html', doc_html.encode(), 'text/html')},
        data={'printBackground': 'true', 'preferCssPageSize': 'true'},
    )
    r.raise_for_status()
    return r.content

async def upload(pdf: bytes, key: str) -> None:
    await asyncio.to_thread(
        _s3.put_object, Bucket=settings.s3_bucket, Key=key, Body=pdf,
        ContentType='application/pdf',
        ContentDisposition=f'attachment; filename="{key.rsplit("/", 1)[-1]}"',
        ContentLanguage='es')

def presign(key: str) -> str:
    return _s3_public.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': settings.s3_bucket,
            'Key': key,
            'ResponseContentDisposition': f'inline; filename="{key.rsplit("/", 1)[-1]}"',
        },
        ExpiresIn=settings.presign_ttl)

async def emit(payload: dict) -> None:
    await _redis.rpush(settings.results_list, json.dumps(payload))

async def close() -> None:
    await _gotenberg.aclose()
    await _redis.aclose()