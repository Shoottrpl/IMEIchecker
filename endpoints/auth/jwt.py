from typing import Any, Dict

import jwt

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from typing_extensions import Annotated

from redis.asyncio import Redis

from endpoints.schemas import UserId
from endpoints.redis_client import get_redis_client
from settings import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Создает JWT токен.

    :param data: Данные для кодирования в токен.
    :return: JWT токен
    """
    to_encode = data.copy()
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt

def verify_token(token: str) -> Dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credential",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except jwt.PyJWTError as e:
        raise credentials_exception

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    redis: Annotated[Redis, Depends(get_redis_client)],
) -> UserId:
    """
    Получает пользователя на основе JWT токена.

    :param token: JWT токен
    :param redis: Клиент редис
    :return: Ошибку если, пользователь не валиден
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credential",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    if not await redis.get(user_id):
        raise credentials_exception

