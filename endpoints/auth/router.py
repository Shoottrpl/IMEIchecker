from typing import Annotated, Dict

from aiohttp.abc import HTTPException
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio import Redis

from bot.logger import LOGS
from endpoints.schemas import UserId
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from .jwt import create_access_token

from database.engine import get_async_session
from database.query import create_user, delete_user, is_whitelisted
from endpoints.redis_client import get_redis_client
from settings import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(
    user_data: UserId,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    redis: Annotated[Redis, Depends(get_redis_client)],
) -> Dict[str, str]:
    """
    Регестрация нового пользователя.

    :param user_data: Данные пользователя, содержащие ID
    :param session: Асинхронная сессия для БД
    :param redis:  Асинхронный клиент Redis
    :return: Сообщение об успешной регестрации
    :raise: Ошибку, если пользователь зарегистрирован или общую ошибку
    """
    user_id = user_data.user_id

    if await is_whitelisted(user_id, session):
        raise HTTPException(
            status_code=status.HTTP_200_OK, detail="You are already registered."
        )

    access_token = create_access_token({"sub": str(user_id)})

    try:
        success = await redis.set(user_id, access_token, ex=settings.expire_time)
        if not success:
            LOGS.info("Failed to save token in Redis")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save token in Redis.",
            )

        await create_user(user_id, session)

        return {"message": "User registered successfully."}

    except Exception as e:
        await redis.delete(user_id)
        await delete_user(user_id, session)
        LOGS.error(f"Error: {e}")

        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {e}",
        )


@router.post("/delete")
async def delete(
    user_data: UserId,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    redis: Annotated[Redis, Depends(get_redis_client)],
) -> Dict[str, str]:
    """
    Удаляет пользователя.

    :param user_data: Данные пользователя, содержащие ID
    :param session: Асинхронная сессия для БД
    :param redis:  Асинхронный клиент Redis
    :return: Сообщение об успешной регестрации
    :raise: Ошибку, если пользователь зарегистрирован или общую ошибку
    """
    user_id = user_data.user_id

    if not await is_whitelisted(user_id, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not register yet."
        )

    try:
        await delete_user(user_id, session)
        await redis.delete(user_id)
        return {"message": "User success deleted."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}"
        )
