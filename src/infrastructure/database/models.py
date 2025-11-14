from sqlalchemy import Column, Integer, String, Boolean
from src.infrastructure.database.base import Base, TimestampMixin


class UserModel(Base, TimestampMixin):
    """SQLAlchemy model for User"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
