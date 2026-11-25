from celery import Celery
from app.redis_client import redis_client
from app.config.settings import settings

celery_app = Celery("backend", broker=settings.celery_broker_url, backend=settings.celery_result_backend)
celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "worker-heartbeat": {
        "task": "backend.heartbeat",
        "schedule": 60.0
    },
}

@celery_app.task(name="backend.heartbeat")
def heartbeat() -> int:
    return redis_client.incr("demo:heartbeat")

