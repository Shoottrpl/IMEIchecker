from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bot.logger import LOGS
from endpoints.auth.jwt import create_access_token
from database.query import is_whitelisted
from settings import settings


async def get_token(redis: Redis, user_id: str) -> str:
    """
    Получает токен пользователя из Redis. Если токена нет, создает новый токен.

    :param redis: Экземпляр Redis
    :param session: Асинхронная сессия БД
    :param user_id: ID пользователя
    :return: Токен пользователя
    """
    token = await redis.get(user_id)

    if token:
        return token


async def update_token(redis: Redis, user_id: str) -> str:
    token = create_access_token({"sub": str(user_id)})
    await redis.set(user_id, token, ex=settings.expire_time)


async def check_access(user_id: int, session: AsyncSession, redis: Redis):
    if not await is_whitelisted(user_id, session):
        return False

    if not await redis.get(user_id):
        await update_token(redis, user_id)

    return True
