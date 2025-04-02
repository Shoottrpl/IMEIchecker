from typing import AsyncGenerator

from redis.asyncio import Redis, ConnectionPool


pool = ConnectionPool.from_url(
    "redis://redis:6379", decode_responses=True, max_connections=10
)


async def get_redis_client() -> AsyncGenerator[Redis, None]:
    """
    Асинхронный генератор, который предоставляет клиент Redis
    :yeild: Асинхронный клиент Redis
    """
    async with Redis(connection_pool=pool) as client:
        yield client
