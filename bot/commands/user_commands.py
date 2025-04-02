from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode

from bot.dialog.states import ImeiSG


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """
    Обрабатывает комманду /start

    Приветсвует пользователя и показывает список комманд

    :param message: Объект сообщения
    :return: Функция ничего не возвращает
    """
    user = message.from_user.username or "Пользователь"

    text = f"""\
                Здравствуй, {user}. Отправь мне imei для проверки.
                \nКомманды бота:
                \nПроверка EMEI - /check
            """

    await message.answer(text)


@router.message(Command("check"))
async def check_handler(
    message: Message,
    dialog_manager: DialogManager,
) -> None:
    """
    Обрабатывает комманду /check

    Запускает диалог проверки IMIE
    :param message: Объект сообщения
    :param dialog_manager: Менеджер диалогов
    :return: Функция ничего не возвращает
    """
    await dialog_manager.start(ImeiSG.imei, mode=StartMode.RESET_STACK)
