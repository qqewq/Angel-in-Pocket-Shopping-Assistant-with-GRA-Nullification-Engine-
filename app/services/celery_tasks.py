from celery import Celery
from ..config import settings

celery_app = Celery(
    "angel_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend="rpc://"
)

@celery_app.task
def recalc_product_safety(product_id: int):
    # Фоновая задача для пересчёта безопасности товара (например, при поступлении нового отзыва)
    # Здесь можно импортировать graph_builder и deal_detector
    pass
