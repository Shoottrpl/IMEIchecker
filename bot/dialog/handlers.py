from typing import Dict
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiohttp import ClientSession
from redis.asyncio import Redis

from constant import CommandMessages
from bot.logger import LOGS
from bot.utils.api_utils import register_from_api, del_from_api, check_imei_from_api
from bot.utils.jwt_utils import get_token
from bot.utils.base_utils import is_valid_imei, template_imei_info, validate_user_id


async def handle_input(
    message: Message, text: ManagedTextInput, manager: DialogManager, input: str
) -> None:
    """
    Обработчик ввода пользователя

    :param message:Объект сообщения
    :param text: Текстовый ввод
    :param manager: Менеджер диалогов
    :param input: Введенные данные
    :return: Функция ничего не возвращает
    """
    manager.show_mode = ShowMode.SEND
    await message.delete()
    await manager.next()


async def add_user_id(
    dialog_manager: DialogManager, session: ClientSession, redis: Redis, **kwargs
) -> Dict[str, str]:
    """
    Добавляет пользователя

    :param dialog_manager: Менеджер диалогов
    :param session: Сессия для работы с API
    :param redis: Клиент Redis
    :param kwargs: Дополнительные аргументы.
    :return: Словарь с результатом выполнения операции
    """
    try:
        user_id: str = dialog_manager.find("user_id").get_value()

        validation_error = validate_user_id(user_id)
        if validation_error:
            return validation_error

        if await redis.get(user_id):
            return {"error": CommandMessages.USER_EXISTS}

        user_id = int(user_id)

        await register_from_api(session, user_id)

        return {"success": CommandMessages.SUCCESS_REGISTRATION}

    except Exception as e:
        LOGS.error(f"Ошибка при обработке комманды /add: {e}")
        return {"error": CommandMessages.GENERAL_ERROR}


async def del_user(
    dialog_manager: DialogManager, session: ClientSession, redis: Redis, **kwargs
) -> Dict[str, str]:
    """
    Удаляет пользователя

    :param dialog_manager: Менеджер диалогов
    :param session: Сессия для работы с API
    :param redis: Клиент Redis
    :param kwargs: Дополнительные аргументы.
    :return: Словарь с результатом выполнения операции
    """
    try:
        user_id: str = dialog_manager.find("user_id").get_value()

        validation_error = validate_user_id(user_id)
        if validation_error:
            return validation_error

        if not await redis.get(user_id):
            return {"error": CommandMessages.USER_NOT_EXISTS}

        user_id = int(user_id)

        await del_from_api(session, user_id)

        return {"success": CommandMessages.SUCCESS_DELETION}

    except Exception as e:
        LOGS.error(f"Ошибка при обработке комманды /del: {e}")
        return {"error": CommandMessages.GENERAL_ERROR}


async def check_imei(
    dialog_manager: DialogManager, session: ClientSession, redis: Redis, **kwargs
) -> Dict[str, str]:
    """
    Проверяет IMEI устройства

    :param dialog_manager: Менеджер диалогов
    :param session: Сессия для работы с API
    :param redis: Клиент Redis
    :param kwargs: Дополнительные аргументы.
    :return: Словарь с результатом выполнения операции
    """
    imei: str = dialog_manager.find("imei").get_value()
    user_id = dialog_manager.event.from_user.id

    if not imei.isdigit() or not is_valid_imei(imei):
        return {"error": CommandMessages.INVALID_IMEI}

    token = await get_token(redis, user_id)
    responce = await check_imei_from_api(session, token, imei)
    LOGS.info(f"{responce}")

    if responce["status"] == "successful":
        text = template_imei_info(responce["properties"])
        return {"result": f"{text}"}
    elif responce["status"] == "unsuccesful":
        return {"error": CommandMessages.EXTERNAL_SERVICE_ERROR}
    return {"error": CommandMessages.GENERAL_ERROR}
