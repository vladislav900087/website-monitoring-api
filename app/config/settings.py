from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str
    cors_origins: list[str]
    jwt_secret_key: str

settings = Settings()