import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import setup_dialogs
from aiohttp import ClientSession
from redis.asyncio import Redis

from settings import settings
from database.engine import async_session_factory

from .middlewares.whitelist_middleware import WhiteListMiddleware
from .logger import LOGS
from .commands import routers
from .dialog.dialogs import register, delete, check
from .initial import UserSetup


async def main() -> None:
    """
    Асинхронная функция для запуска бота.

    Инициализирует Redis, бота и запускает pooling чтобы слушать обновления
    :return: Ничего не возвращает
    """
    redis = Redis(host="redis", decode_responses=True)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(WhiteListMiddleware())

    dp.include_routers(*routers, register, delete, check)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    async with ClientSession(base_url=settings.proxy_url) as session:
        await UserSetup(session)
        await dp.start_polling(
            bot,
            db_sessionmaker=async_session_factory,
            redis=redis,
            session=session,
            allowed_updates=dp.resolve_used_update_types(),
        )


if __name__ == "__main__":
    """
    Точка входа в приложение
    """
    LOGS.info("Start Bot")
    asyncio.run(main())
