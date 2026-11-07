from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    redis_url: str = 'redis://redis:6379'
    queue_name: str = 'report-queue'
    queue_prefix: str = 'bull'
    results_list: str = 'report-results'

    s3_endpoint: str = 'http://minio:9000'
    s3_public_endpoint: str = 'http://localhost:9000'
    s3_bucket: str = 'reports'
    minio_root_user: str = 'admin'
    minio_root_password: str = ''
    presign_ttl: int = 86_400

    gotenberg_url: str = 'http://gotenberg:3000'
    gotenberg_timeout: int = 90

    ai_model: str = 'deepseek-v4-pro'
    ai_timeout: int = 300
    max_tokens: int = 12_000
    concurrency: int = Field(default=8, ge=1, le=32)
    shutdown_timeout: int = 110
    log_level: str = 'INFO'

settings = Settings()