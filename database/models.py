from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from endpoints.auth.jwt import create_access_token
from settings import settings


class Whitelist(Base):
    """
    Модель для хранения ID пользователя в белом списке
    """

    __tablename__ = "whitelist"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )
