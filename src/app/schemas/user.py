from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from config.db import Base
import uuid


class User(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    hashed_password = Column(String)
    full_name = Column(String)
    email = Column(String)
    disabled = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), default=func.now())

    def __init__(self, username, hashed_password, full_name, email, disabled):
        self.username = username
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.email = email
        self.disabled = disabled
