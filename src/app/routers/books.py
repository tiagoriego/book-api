from fastapi import APIRouter, HTTPException, Depends, status, Response
from services import book_service, link_service
from config.headers import get_current_user
from models.book import Book, BookUpdate
from models.link import Link
from schemas.book import Book as BookSchema
from schemas.link import Link as LinkSchema

router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_current_user)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
)


def get_book_by_id(book_id: str) -> BookSchema | HTTPException:
    book = book_service.get_book_by_id(book_id=book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


def get_link_by_id(link_id: str) -> LinkSchema | HTTPException:
    link = link_service.get_link_by_id(link_id=link_id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return link


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
    book = get_book_by_id(book_id=book_id)
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
    get_book_by_id(book_id=book_id)
    book_service.delete_book(book_id=book_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_id: str, book: BookUpdate):

    old_book = get_book_by_id(book_id=book_id)

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


@router.get("/{book_id}/links", response_model=list[Link])
async def get_all_book_links(book_id: str):
    book = get_book_by_id(book_id=book_id)
    links = link_service.get_all_link(book_id=book.id)
    result: list[Link] = []
    for link in links:
        result.append(Link(
            id=link.id,
            book_id=link.book_id,
            name=link.name,
            url=link.url
        ))

    return result


@router.post("/{book_id}/links", response_model=Link, status_code=status.HTTP_201_CREATED)
async def create_book_link(book_id: str, link: Link):
    book = get_book_by_id(book_id=book_id)
    new_link = LinkSchema(
        book_id=book.id,
        name=link.name,
        url=link.url
    )
    result = link_service.create_link(new_link)
    return Link(
        id=result.id,
        book_id=result.book_id,
        name=link.name,
        url=result.url
    )


@router.delete("/{book_id}/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_link(book_id: str, link_id: str):
    get_book_by_id(book_id=book_id)
    get_link_by_id(link_id=link_id)
    link_service.delete_link(link_id=link_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
