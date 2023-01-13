from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from config.db import Base
import uuid


class Link(Base):

    __tablename__ = "links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(String, ForeignKey("books.id", ondelete="CASCADE"))
    name = Column(String)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), default=func.now())

    def __init__(self, book_id, name, url):
        self.book_id = book_id
        self.name = name
        self.url = url
