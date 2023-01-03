from fastapi import APIRouter, HTTPException, Depends, status, Response
from services import book_service
from config.headers import get_current_user
from models.book import Book, BookUpdate
from schemas.book import Book as BookSchema

router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_current_user)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)


@router.get("/", response_model=list[Book])
async def get_all_book():
    list_book = book_service.get_all_book()
    result: list[Book] = []
    for book in list_book:
        result.append(Book(
            id=book.id,
            title=book.title,
            author=book.author,
            dimensions=book.dimensions,
            format=book.format,
            isbn=book.isbn,
            language=book.language,
            paperback=book.paperback,
            publication_date=book.publication_date,
            publisher=book.publisher
        ))
    return result


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str):
    book = book_service.get_book_by_id(book_id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    result = Book(
        id=book.id,
        title=book.title,
        author=book.author,
        dimensions=book.dimensions,
        format=book.format,
        isbn=book.isbn,
        language=book.language,
        paperback=book.paperback,
        publication_date=book.publication_date,
        publisher=book.publisher
    )
    return result


@router.post("/", response_model=Book)
async def create_book(book: Book):
    new_book = BookSchema(
        title=book.title,
        author=book.author,
        dimensions=book.dimensions,
        format=book.format,
        isbn=book.isbn,
        language=book.language,
        paperback=book.paperback,
        publication_date=book.publication_date,
        publisher=book.publisher
    )
    result = book_service.create_book(new_book)
    book.id = str(result.id)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str):
    book = book_service.get_book_by_id(book_id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    book_service.delete_book(book_id=book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: str, book: BookUpdate):

    old_book = book_service.get_book_by_id(book_id=book_id)
    if not old_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if not book.title:
        book.title = old_book.title

    if not book.author:
        book.author = old_book.author

    if not book.dimensions:
        book.dimensions = old_book.dimensions

    if not book.format:
        book.format = old_book.format

    if not book.isbn:
        book.isbn = old_book.isbn

    if not book.language:
        book.language = old_book.language

    if not book.paperback:
        book.paperback = old_book.paperback

    if not book.publication_date:
        book.publication_date = old_book.publication_date

    if not book.publisher:
        book.publisher = old_book.publisher

    old_book.title = book.title
    old_book.author = book.author
    old_book.dimensions = book.dimensions
    old_book.format = book.format
    old_book.isbn = book.isbn
    old_book.language = book.language
    old_book.paperback = book.paperback
    old_book.publication_date = book.publication_date
    old_book.publisher = book.publisher

    book_service.update_book(book=old_book)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
