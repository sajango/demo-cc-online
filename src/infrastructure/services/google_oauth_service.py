from typing import Optional, Dict, Any
import httpx
from jose import jwt, JWTError
from src.core.config import settings


class GoogleOAuthService:
    """Service for Google OAuth authentication"""

    GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID

    async def verify_id_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Google ID token and extract user info

        Args:
            id_token: Google ID token from client

        Returns:
            Dictionary with user info or None if invalid
        """
        try:
            # Fetch Google's public keys
            async with httpx.AsyncClient() as client:
                response = await client.get(self.GOOGLE_CERTS_URL)
                google_certs = response.json()

            # Decode and verify the token
            # Note: In production, you should cache the keys
            header = jwt.get_unverified_header(id_token)
            key = None

            for cert in google_certs.get("keys", []):
                if cert.get("kid") == header.get("kid"):
                    key = cert
                    break

            if not key:
                return None

            # Verify token
            payload = jwt.decode(
                id_token,
                key,
                algorithms=["RS256"],
                audience=self.client_id,
                options={"verify_at_hash": False},
            )

            # Validate issuer
            if payload.get("iss") not in ["https://accounts.google.com", "accounts.google.com"]:
                return None

            # Extract user information
            return {
                "email": payload.get("email"),
                "full_name": payload.get("name", ""),
                "provider_user_id": payload.get("sub"),
                "email_verified": payload.get("email_verified", False),
                "picture": payload.get("picture"),
            }

        except JWTError:
            return None
        except Exception:
            return None

    async def get_user_info_from_access_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get user info from Google using access token

        Args:
            access_token: Google access token

        Returns:
            Dictionary with user info or None if invalid
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.GOOGLE_USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"}
                )

                if response.status_code != 200:
                    return None

                user_info = response.json()

                return {
                    "email": user_info.get("email"),
                    "full_name": user_info.get("name", ""),
                    "provider_user_id": user_info.get("sub"),
                    "email_verified": user_info.get("email_verified", False),
                    "picture": user_info.get("picture"),
                }

        except Exception:
            return None
