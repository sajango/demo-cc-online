from typing import Optional, Dict, Any
import httpx
from jose import jwt, JWTError
from src.core.config import settings


class AppleOAuthService:
    """Service for Apple Sign-In authentication"""

    APPLE_PUBLIC_KEYS_URL = "https://appleid.apple.com/auth/keys"
    APPLE_ISSUER = "https://appleid.apple.com"

    def __init__(self):
        self.client_id = settings.APPLE_CLIENT_ID
        self.team_id = settings.APPLE_TEAM_ID

    async def verify_id_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Apple ID token and extract user info

        Args:
            id_token: Apple ID token from client

        Returns:
            Dictionary with user info or None if invalid
        """
        try:
            # Fetch Apple's public keys
            async with httpx.AsyncClient() as client:
                response = await client.get(self.APPLE_PUBLIC_KEYS_URL)
                apple_keys = response.json()

            # Decode and verify the token
            header = jwt.get_unverified_header(id_token)
            key = None

            for apple_key in apple_keys.get("keys", []):
                if apple_key.get("kid") == header.get("kid"):
                    key = apple_key
                    break

            if not key:
                return None

            # Verify token
            payload = jwt.decode(
                id_token,
                key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=self.APPLE_ISSUER,
            )

            # Validate issuer
            if payload.get("iss") != self.APPLE_ISSUER:
                return None

            # Extract user information
            # Note: Apple only provides email and may provide name on first sign-in
            email = payload.get("email")
            provider_user_id = payload.get("sub")

            if not email or not provider_user_id:
                return None

            return {
                "email": email,
                "full_name": "",  # Apple doesn't always provide name in token
                "provider_user_id": provider_user_id,
                "email_verified": payload.get("email_verified", "false") == "true",
                "is_private_email": payload.get("is_private_email", "false") == "true",
            }

        except JWTError:
            return None
        except Exception:
            return None

    def extract_user_info_from_response(
        self, id_token_payload: Dict[str, Any], user_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract user info from Apple Sign-In response

        Args:
            id_token_payload: Decoded ID token payload
            user_data: Optional user data from first-time sign-in

        Returns:
            Dictionary with user info
        """
        email = id_token_payload.get("email", "")
        provider_user_id = id_token_payload.get("sub", "")

        # On first sign-in, Apple may provide name in separate user object
        full_name = ""
        if user_data:
            name = user_data.get("name", {})
            first_name = name.get("firstName", "")
            last_name = name.get("lastName", "")
            full_name = f"{first_name} {last_name}".strip()

        return {
            "email": email,
            "full_name": full_name or email.split("@")[0],  # Use email prefix if no name
            "provider_user_id": provider_user_id,
            "email_verified": id_token_payload.get("email_verified", "false") == "true",
            "is_private_email": id_token_payload.get("is_private_email", "false") == "true",
        }
