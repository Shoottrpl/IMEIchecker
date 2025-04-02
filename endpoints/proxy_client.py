import newrelic.agent

from typing import Annotated, Dict, Union

from fastapi import FastAPI, Depends
from fastapi.middleware.gzip import GZipMiddleware

from settings import settings

from .schemas import IMEI, UserId
from .imei_checker import IMEICheckClient
from .auth.router import router as auth_router
from .auth.jwt import get_current_user


imei_api = IMEICheckClient(base_url=settings.api_base_url, api_key=settings.api_token)

app = FastAPI()

app.add_middleware(GZipMiddleware, compresslevel=6)
app.include_router(auth_router)


@app.post("/api/check-imei")
async def check_imei(
    imei: IMEI, user_id: Annotated[UserId, Depends(get_current_user)]
) -> Dict[str, Union[str, Dict]]:
    """
    Проверяет IMEI устройства и валидность текущего пользователя
    :param imei: IMEI устройства
    :param user_id: ID пользователя
    :return: Словарь с результатами проверки
    """
    responce = await imei_api.check(imei.imei)
    return responce
