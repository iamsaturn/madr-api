from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class NovelistCreate(BaseModel):
    name: str

class NovelistPublic(BaseModel):
    name: str
    id: int
    model_config = ConfigDict(from_attributes=True)

class NovelistUpdate(BaseModel):
    name: str | None = None

class BookCreate(BaseModel):
    title: str
    year: int
    novelist_id: int

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