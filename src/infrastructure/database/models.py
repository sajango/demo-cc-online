import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.mysql import CHAR
from src.infrastructure.database.base import Base, TimestampMixin


class UserModel(Base, TimestampMixin):
    """SQLAlchemy model for User"""

    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
