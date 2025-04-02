from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings

# Создание асинхронного движка
engine = create_async_engine(
    url=settings.database_url,
    echo=True,
)

# Фабрика асинхронных сессий
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор, который предоставляет сессию для работы с БД.

    :yield: Асинхронная сессия для работы с БД
    """
    async with async_session_factory() as session:
        yield session
