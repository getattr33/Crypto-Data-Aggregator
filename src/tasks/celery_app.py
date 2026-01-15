from celery import Celery
from src.config import settings

celery_app = Celery(
    "src.tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include="src.tasks.fetch_prices",
)
celery_app.conf.beat_schedule = {
    "fetch_prices": {
        "task": "fetch_prices_task",
        "schedule": 60,
    }
}
