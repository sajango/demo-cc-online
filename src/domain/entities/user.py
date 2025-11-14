from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User domain entity"""

    id: Optional[str] = None
    email: str = ""
    username: str = ""
    full_name: str = ""
    password_hash: Optional[str] = None
    auth_provider: str = "local"
    oauth_provider_id: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def activate(self) -> None:
        """Activate user account"""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate user account"""
        self.is_active = False

    def verify(self) -> None:
        """Verify user account"""
        self.is_verified = True
