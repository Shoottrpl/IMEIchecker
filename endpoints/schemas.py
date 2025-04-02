from pydantic import BaseModel


class UserId(BaseModel):
    """Модель представления ID пользователя"""

    user_id: int


# class Token(BaseModel):
#     """Модель представления токена"""
#     access_token: str
#     token_type: str


class IMEI(BaseModel):
    """Модель представления IMEI"""

    imei: str
