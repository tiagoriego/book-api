from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from config.db import Base
import uuid


class Book(Base):

    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    author = Column(String)
    dimensions = Column(String)
    format = Column(String)
    isbn = Column(String)
    language = Column(String)
    paperback = Column(String)
    publication_date = Column(String)
    publisher = Column(String)

    def __init__(self, title, author, dimensions, format,
                 isbn, language, paperback, publication_date, publisher):
        self.title = title
        self.author = author
        self.dimensions = dimensions
        self.format = format
        self.isbn = isbn
        self.language = language
        self.paperback = paperback
        self.publication_date = publication_date
        self.publisher = publisher
