from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    """Schema for user registration"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""

    refresh_token: str


class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth request"""

    id_token: str


class AppleAuthRequest(BaseModel):
    """Schema for Apple Sign-In request"""

    id_token: str
    code: Optional[str] = None


class OAuthUserInfo(BaseModel):
    """Schema for OAuth user information"""

    email: EmailStr
    full_name: str
    provider: str
    provider_user_id: str
