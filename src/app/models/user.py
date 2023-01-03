from pydantic import BaseModel


class User(BaseModel):

    id: str
    full_name: str
    username: str
    email: str
