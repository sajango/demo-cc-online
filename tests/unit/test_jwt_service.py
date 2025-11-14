import pytest
from datetime import timedelta
from src.infrastructure.services.jwt_service import JWTService


def test_create_access_token():
    """Test access token creation"""
    jwt_service = JWTService()
    data = {"sub": "user123", "email": "test@example.com"}

    token = jwt_service.create_access_token(data)

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_refresh_token():
    """Test refresh token creation"""
    jwt_service = JWTService()
    data = {"sub": "user123"}

    token = jwt_service.create_refresh_token(data)

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_valid_token():
    """Test decoding a valid token"""
    jwt_service = JWTService()
    data = {"sub": "user123", "email": "test@example.com"}

    token = jwt_service.create_access_token(data)
    decoded = jwt_service.decode_token(token)

    assert decoded is not None
    assert decoded["sub"] == "user123"
    assert decoded["email"] == "test@example.com"
    assert decoded["type"] == "access"


def test_decode_invalid_token():
    """Test decoding an invalid token"""
    jwt_service = JWTService()

    decoded = jwt_service.decode_token("invalid.token.here")

    assert decoded is None


def test_verify_access_token():
    """Test verifying an access token"""
    jwt_service = JWTService()
    data = {"sub": "user123"}

    token = jwt_service.create_access_token(data)
    payload = jwt_service.verify_token(token, token_type="access")

    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["type"] == "access"


def test_verify_refresh_token():
    """Test verifying a refresh token"""
    jwt_service = JWTService()
    data = {"sub": "user123"}

    token = jwt_service.create_refresh_token(data)
    payload = jwt_service.verify_token(token, token_type="refresh")

    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["type"] == "refresh"


def test_verify_wrong_token_type():
    """Test verifying token with wrong type"""
    jwt_service = JWTService()
    data = {"sub": "user123"}

    # Create access token but verify as refresh
    access_token = jwt_service.create_access_token(data)
    payload = jwt_service.verify_token(access_token, token_type="refresh")

    assert payload is None


def test_custom_expiration():
    """Test token creation with custom expiration"""
    jwt_service = JWTService()
    data = {"sub": "user123"}
    custom_expiry = timedelta(minutes=5)

    token = jwt_service.create_access_token(data, expires_delta=custom_expiry)
    decoded = jwt_service.decode_token(token)

    assert decoded is not None
    assert "exp" in decoded
