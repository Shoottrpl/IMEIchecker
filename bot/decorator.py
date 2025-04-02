from functools import wraps
from typing import Callable, ParamSpec, TypeVar
from aiogram.types import Message

from settings import settings


P = ParamSpec("P")
R = TypeVar("R")


def admin_only(func: Callable[P, R]) -> Callable[P, R]:
    """
    Декоратор для ограничения  доступа к коммандам бота

    :param func: Функция которую нужно обернуть
    :return: Обернутая функция
    """

    @wraps(func)
    async def wrapper(message: Message, *args: P.args, **kwargs: P.kwargs) -> R:
        """
        Функция обертка
        :param message: Объект сообщения от пользователя
        :param args: Позиционные аргументы
        :param kwargs: Именнованые аргументы
        :return: Результат выполнения функции
        """
        if message.from_user.id != settings.owner_id:
            await message.answer("У вас нет прав на выполнение этой команды.")
            return

        return await func(message, *args, **kwargs)

    return wrapper
