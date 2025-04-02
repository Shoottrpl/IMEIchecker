import asyncio
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from redis.asyncio import Redis

from database.engine import get_async_session
from endpoints.proxy_client import app
from endpoints.redis_client import get_redis_client


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def mock_is_whitelisted(mocker):
    mock = AsyncMock(return_value=False)
    mocker.patch("database.query.is_whitelisted", mock)
    return mock

@pytest_asyncio.fixture
async def mock_session():
    session = AsyncMock(spec=AsyncSession)
    session.get = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest_asyncio.fixture
async def mock_redis():
    redis = AsyncMock(spec=Redis)
    redis.set = AsyncMock()
    redis.delete = AsyncMock()
    return redis

@pytest_asyncio.fixture
def client(mock_session, mock_redis):
    app.dependency_overrides[get_async_session] = lambda: mock_session
    app.dependency_overrides[get_redis_client] = lambda: mock_redis
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(autouse=True)
def cleanup(mock_session, mock_redis):
    original_session_get = mock_session.get.return_value
    original_redis_set = mock_redis.set.return_value

    yield

    mock_session.reset_mock()
    mock_redis.reset_mock()
    mock_session.get.return_value = original_session_get
    mock_redis.set.return_value = original_redis_set