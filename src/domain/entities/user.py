from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User domain entity"""

    id: Optional[int] = None
    email: str = ""
    username: str = ""
    full_name: str = ""
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def activate(self) -> None:
        """Activate user account"""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate user account"""
        self.is_active = False
