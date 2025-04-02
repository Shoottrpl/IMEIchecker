from aiohttp import ClientSession

from .utils.api_utils import register_from_api
from settings import settings
from .logger import LOGS


async def _OwnerUsers(session: ClientSession) -> None:
    """
    Регистрирует владельца бота через API
    :param session: Сессия aiohttp для выполнения HTTP-запросов.
    :return: Если регистрация не успешная логирует ошибку
    """
    try:
        await register_from_api(session, settings.owner_id)
        LOGS.info("Added white users")
    except Exception as e:
        LOGS.error(f"Error while adding white users: {e}")


async def UserSetup(session: ClientSession) -> None:
    LOGS.info("Setting Up Users")
    await _OwnerUsers(session)
