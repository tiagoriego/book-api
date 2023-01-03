from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):

    id: Optional[str]
    title: str
    author: str
    dimensions: str
    format: str
    isbn: str
    language: str
    paperback: str
    publication_date: str
    publisher: str


class BookUpdate(BaseModel):

    title: Optional[str]
    author: Optional[str]
    dimensions: Optional[str]
    format: Optional[str]
    isbn: Optional[str]
    language: Optional[str]
    paperback: Optional[str]
    publication_date: Optional[str]
    publisher: Optional[str]
