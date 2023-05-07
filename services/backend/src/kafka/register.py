from typing import Optional
from aiokafka import AIOKafkaProducer

async def init_kafka_producer(config: Optional[dict] = None) -> AIOKafkaProducer:
    producer = AIOKafkaProducer(**config)
    await producer.start()
    return producer

async def close_kafka_producer(producer: AIOKafkaProducer) -> None:
    await producer.stop()

def register_kafka(app, config: Optional[dict] = None) -> None:
    @app.on_event("startup")
    async def startup_event():
        app.state.producer = await init_kafka_producer(config)

    @app.on_event("shutdown")
    async def shutdown_event():
        await close_kafka_producer(app.state.producer)
