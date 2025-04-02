from typing import Union, Dict

from tenacity import retry, stop_after_attempt, wait_exponential
from aiohttp import ClientSession

from bot.logger import LOGS
from settings import settings


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
async def register_from_api(
    session: ClientSession,
    user_id: int,
) -> Union[Dict[str, str] | str]:
    """
    Регестрация пользователя через API

    :param session: Сессия для работы с API
    :param user_id: ID пользователя
    :return: Cообщение об успехе или ошибке
    """
    data = {"user_id": user_id}

    async with session.post("/auth/register", json=data) as r:
        if r.status != 200:
            LOGS.info(f"{await r.json()}")
            return {"error": f"Ошибка: статус {r.status}"}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def del_from_api(
    session: ClientSession,
    user_id: int,
) -> Union[Dict[str, str] | str]:
    """
    Удаляет пользователя через API

    :param session: Сессия для работы с API
    :param user_id: ID пользователя
    :return: Cообщение об успехе или ошибке
    """
    data = {"user_id": user_id}
    async with session.post("/auth/delete", json=data) as r:
        if r.status != 200:
            LOGS.info(f"{await r.json()}")
            return {"error": f"Ошибка: статус {r.status}"}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def check_imei_from_api(
    session: ClientSession,
    api_token: str,
    imei: str,
) -> Dict[str, str]:
    """
    Проверка IMEI через API

    :param session: Сессия для работы с API
    :param api_token: Токен доступа
    :param imei: IMEI устройста
    :return: Результат проверки IMEI
    """
    async with session.post(
        url="/api/check-imei",
        json={"imei": imei},
        headers={"Authorization": f"Bearer {api_token}"},
    ) as r:
        LOGS.info(f"{r.status}")
        res = await r.json()
        return res
