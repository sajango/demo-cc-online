import pytest
from src.domain.entities.user import User


def test_user_creation():
    """Test user entity creation"""
    user = User(
        id="550e8400-e29b-41d4-a716-446655440000",
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        is_active=True,
    )

    assert user.id == "550e8400-e29b-41d4-a716-446655440000"
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.full_name == "Test User"
    assert user.is_active is True


def test_user_activate():
    """Test user activation"""
    user = User(is_active=False)
    user.activate()
    assert user.is_active is True


def test_user_deactivate():
    """Test user deactivation"""
    user = User(is_active=True)
    user.deactivate()
    assert user.is_active is False
