import logging

import aiokafka

from app.core import config
from app.core.config import settings

KAFKA_MATH_TOPIC = 'math'

logger = logging.getLogger(config.LOGGER_NAME)

_connected = False
_producer = None


async def start():
    global _producer
    _producer = aiokafka.AIOKafkaProducer(
        bootstrap_servers=f"{settings.KAFKA_SERVER}:{settings.KAFKA_PORT}"
    )
    await _producer.start()
    # if producer can not connect exception will be raised and
    # _connected will be never ste to true
    global _connected
    _connected = True


async def stop():
    global _producer
    if isinstance(_producer, aiokafka.AIOKafkaProducer):
        await _producer.stop()


async def send_math_event(msj: str):
    if isinstance(_producer, aiokafka.AIOKafkaProducer) and _connected:
        await _producer.send(KAFKA_MATH_TOPIC, msj)
    else:
        logger.warning(f"Can not send event <{msj}> because broker connection failed.")
