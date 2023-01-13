from pydantic import BaseModel
from typing import Optional


class Link(BaseModel):

    id: Optional[str]
    book_id: Optional[str]
    name: str
    url: str
