from typing import Dict, Union, Optional

from newrelic.agent import ExternalTrace
from aiohttp import ClientSession

from .schemas import IMEI


class Client:
    """Клиент для выполнения HTTP запросов"""

    def __init__(self, base_url: str, api_key: str):
        """
        Инициализация клиента
        :param base_url: Базовый URL для API
        :param api_key: API ключ для аутентификации
        """
        self.base_url = base_url
        self.api_key = api_key
        self._session: Optional[ClientSession] = None

    async def get_session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession(
                base_url=self.base_url,
                headers={
                    "Authorization": "Bearer " + self.api_key,
                    "Content-Type": "application/json",
                },
            )
        return self._session

    async def close(self):
        if self._session:
            await self._session.close()


class IMEICheckClient(Client):
    """Клиент для проверки IMEI через API"""

    async def check(self, imei: IMEI) -> Dict[str, Union[str, Dict]]:
        """
        Проверка IMEI

        :param imei: IMEI устройства
        :return: Словарь с результатом, со статусом и свойствами
        """
        session = await self.get_session()

        async with session.post(
            url="/v1/checks",
            json={
                "deviceId": imei,
                "serviceId": 12,
                "fields": ["status", "properties"],
            },
        ) as responce:
            result = await responce.json()

            return {"status": result["status"], "properties": result["properties"]}
