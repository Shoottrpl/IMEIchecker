from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from redis.asyncio import Redis

from bot.dialog.states import RegisterSG, DeleteSG
from bot.decorator import admin_only

router = Router()


@router.message(Command("add"))
@admin_only
async def cmd_add(
    message: Message,
    redis: Redis,
    dialog_manager: DialogManager,
) -> None:
    """
    Обработчик комманды /add

    Запускает диалог регистрации пользователя

    :param message: Объект сообщения
    :param redis: Клиент Redis для работы с данными
    :param dialog_manager: Менеджер диалогов
    :return: Функция ничего не возвращает
    """
    await dialog_manager.start(RegisterSG.user_id, mode=StartMode.RESET_STACK)


@router.message(Command("del"))
@admin_only
async def cmd_del(
    message: Message,
    redis: Redis,
    dialog_manager: DialogManager,
) -> None:
    """
    Обработчик комманды /add

    Запускает диалог удаления пользователя

    :param message: Объект сообщения
    :param redis: Клиент Redis для работы с данными
    :param dialog_manager: Менеджер диалогов
    :return: Функция ничего не возвращает
    """
    await dialog_manager.start(DeleteSG.user_id, mode=StartMode.RESET_STACK)
