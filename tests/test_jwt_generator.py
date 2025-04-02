import pytest
from endpoints.auth.jwt import create_access_token, verify_token


def test_create_access_token():
    token = create_access_token({"sub": "test"})
    assert isinstance(token, str)
    assert len(token.split(".")) == 3



def test_token_verification():
    token = create_access_token({"sub": "test"})
    decode = verify_token(token)
    assert decode["sub"] == "test"