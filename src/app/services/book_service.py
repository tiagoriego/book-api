from config.db import Session
from schemas.book import Book

session = Session()


def get_all_book() -> list[Book]:
    books = session.query(Book).order_by(Book.created_at.desc()).all()
    return books


def get_book_by_id(book_id: str) -> Book:
    book = session.query(Book).filter_by(id=book_id).first()
    return book


def create_book(book: Book) -> Book:
    try:
        session.add(book)
        session.flush()
        book_id = str(book.id)
        session.commit()
        new_book = session.query(Book).filter_by(id=book_id).first()
    except Exception as e:
        session.rollback()
        raise Exception("Failed create_book", e)
    return new_book


def update_book(book: Book) -> bool:
    try:
        session.add(book)
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Failed update_book", e)
    return True


def delete_book(book_id: str):
    try:
        session.query(Book).filter_by(id=book_id).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Failed delete_book", e)
