import pytest
from src.infrastructure.services.password_service import PasswordService


def test_password_hashing():
    """Test password hashing"""
    password_service = PasswordService()
    plain_password = "SecurePassword123!"

    # Hash the password
    hashed = password_service.hash_password(plain_password)

    # Verify the hash is different from plain password
    assert hashed != plain_password
    assert len(hashed) > 0


def test_password_verification_success():
    """Test successful password verification"""
    password_service = PasswordService()
    plain_password = "SecurePassword123!"

    # Hash and verify
    hashed = password_service.hash_password(plain_password)
    assert password_service.verify_password(plain_password, hashed) is True


def test_password_verification_failure():
    """Test failed password verification"""
    password_service = PasswordService()
    plain_password = "SecurePassword123!"
    wrong_password = "WrongPassword456!"

    # Hash with correct password, verify with wrong password
    hashed = password_service.hash_password(plain_password)
    assert password_service.verify_password(wrong_password, hashed) is False


def test_different_hashes_for_same_password():
    """Test that same password produces different hashes (salt)"""
    password_service = PasswordService()
    plain_password = "SecurePassword123!"

    hash1 = password_service.hash_password(plain_password)
    hash2 = password_service.hash_password(plain_password)

    # Different hashes due to salt
    assert hash1 != hash2

    # But both should verify correctly
    assert password_service.verify_password(plain_password, hash1) is True
    assert password_service.verify_password(plain_password, hash2) is True
