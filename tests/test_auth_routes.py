import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_register_user(client, mock_session, mock_redis, mock_is_whitelisted):
    mock_session.execute.return_value = False
    mock_redis.set.return_value = True

    response = client.post(
        "/auth/register",
        json={"user_id": 123},

    )

    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully."}



