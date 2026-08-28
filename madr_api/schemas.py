from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def sanitize_text(value: str) -> str:
    value = value.lower().strip().split()
    value = " ".join(value)
    return value


class NovelistCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, value: str):
        return sanitize_text(value)


class NovelistPublic(BaseModel):
    name: str
    id: int
    model_config = ConfigDict(from_attributes=True)


class NovelistUpdate(BaseModel):
    name: str | None = None

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, value: str):
        if value is None:
            return value
        return sanitize_text(value)


class BookCreate(BaseModel):
    title: str
    year: int
    novelist_id: int

    @field_validator("title")
    @classmethod
    def sanitize_title(cls, value: str):
        return sanitize_text(value)


class BookPublic(BaseModel):
    id: int
    title: str
    year: int
    novelist: NovelistPublic
    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    title: str | None = None
    year: int | None = None
    novelist_id: int | None = None

    @field_validator("title")
    @classmethod
    def sanitize_title(cls, value: str):
        if value is None:
            return value
        return sanitize_text(value)


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class Token_Schema(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(20, ge=1)


class NovelistFilter(FilterPage):
    name: str | None = None


class BookFilter(FilterPage):
    title: str | None = None
    year: int | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
