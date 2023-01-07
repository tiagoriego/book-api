from pydantic import BaseModel, validator, Field


class User(BaseModel):

    id: str
    full_name: str
    username: str
    email: str


class UpdateUser(BaseModel):

    full_name: str
    email: str


class UpdatePassowrd(BaseModel):

    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)

    @validator("new_password", "old_password", pre=True, always=True)
    def remove_whitespace(cls, value: str) -> str | None:
        return value.replace(" ", "")
