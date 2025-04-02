from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from .models import Whitelist
from bot.logger import LOGS


async def create_user(new_user_id: int, session: AsyncSession) -> None:
    """
    Создание нового пользователя в белом списке

    :param new_user_id: ID пользователя
    :param session: Асинхронная сессия
    :return: Ничего
    """
    try:
        user = Whitelist(user_id=new_user_id)

        session.add(user)
        await session.commit()
        LOGS.info(f"User  {user.user_id} saved successfully.")
    except Exception as e:
        await session.rollback()
        LOGS.error(f"Error: {e}")


async def delete_user(user_id: int, session: AsyncSession) -> bool:
    """
    Удаление пользователя из белого списка.

    :param user_id: ID пользователя
    :param session: Асинхронная сессия
    :return: True если пользователь удален, либо False
    """
    try:
        user = await get_user(user_id, session)

        if user:
            await session.delete(user)
            await session.commit()
            return True

    except Exception as e:
        await session.rollback()
        LOGS.error(f"Error: {e}")
        return False


async def get_user(user_id: int, session: AsyncSession) -> Optional[Whitelist]:
    """
    Получение пользователя из белого списка по ID.

    :param user_id: ID пользователя
    :param session: Асинхронная сессия
    :return: Объект пользователя, либо None
    """
    query = select(Whitelist).where(Whitelist.user_id == user_id)
    return await session.scalar(query)


async def is_whitelisted(user_id: int, session: AsyncSession) -> bool:
    """
    Проверка находится ID пользователя в белом списке.

    :param user_id: ID пользователя
    :param session: Асинхронная сессия
    :return: True если пользователь в белом списке, либо False
    """
    user = await session.get(Whitelist, user_id)
    return user is not None
