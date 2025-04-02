from aiogram import BaseMiddleware
from redis.asyncio import Redis
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio import AsyncSession

from bot.logger import LOGS
from bot.utils.jwt_utils import update_token, check_access
from database.query import is_whitelisted


class WhiteListMiddleware(BaseMiddleware):
    """
    Middleware для проверки, пользователя в whitelist
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Обрабатывает входящее событие

        :param handler: Обработчик события
        :param event: Входящее событие
        :param data: Данные события
        :return: Результат выполнения обработчика или None
        """
        bot = data["bot"]
        redis: Redis = data["redis"]
        db_sessionmaker: AsyncSession = data["db_sessionmaker"]
        user_id: int = data["event_from_user"].id

        async with db_sessionmaker() as session:
            if not await check_access(user_id, session, redis):
                LOGS.info(f"User not in whitelist")
                await bot.send_message(user_id, "Доступ запрещен. Вы не в whitelist.")
                return None

        return await handler(event, data)
