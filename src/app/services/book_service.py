from config.db import Session
from schemas.book import Book

session = Session()


def get_all_book() -> list[Book]:
    books = session.query(Book).all()
    return books


def get_book_by_id(book_id) -> Book:
    book = session.query(Book).filter_by(id=book_id).first()
    return book


def create_book(book: Book) -> Book:
    session.add(book)
    session.flush()
    book_id = str(book.id)
    session.commit()
    new_book = session.query(Book).filter_by(id=book_id).first()
    return new_book


def update_book(book: Book) -> bool:
    session.add(book)
    session.flush()
    session.commit()
    return True


def delete_book(book_id: str):
    session.query(Book).filter_by(id=book_id).delete()
    session.commit()
