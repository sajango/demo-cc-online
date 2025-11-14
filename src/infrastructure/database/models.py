import uuid
import enum
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.dialects.mysql import CHAR
from src.infrastructure.database.base import Base, TimestampMixin


class AuthProvider(enum.Enum):
    """Authentication provider enum"""

    LOCAL = "local"
    GOOGLE = "google"
    APPLE = "apple"


class UserModel(Base, TimestampMixin):
    """SQLAlchemy model for User"""

    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=True)  # Nullable for OAuth users
    auth_provider = Column(Enum(AuthProvider), default=AuthProvider.LOCAL, nullable=False)
    oauth_provider_id = Column(String(255), nullable=True, index=True)  # OAuth user ID
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
