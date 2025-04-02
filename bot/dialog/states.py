from aiogram.filters.state import State, StatesGroup


class TokenSG(StatesGroup):
    """
    Группа состояний для токенов
    """

    main = State()


class RegisterSG(StatesGroup):
    """
    Группа состояний для регестрации
    """

    user_id = State()
    token = State()


class DeleteSG(StatesGroup):
    """
    Группа состояний для удаления
    """

    user_id = State()
    result = State()


class ImeiSG(StatesGroup):
    """
    Группа состояний для проверки IMIE
    """

    imei = State()
    result = State()
