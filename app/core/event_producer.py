from kafka import KafkaProducer

from app.core.config import settings

producer = KafkaProducer(
    api_version=(7, 0, 1),
    bootstrap_servers=f"{settings.KAFKA_SERVER}:{settings.KAFKA_PORT}"
)
