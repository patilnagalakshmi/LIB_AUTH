from pydantic import BaseModel
from typing import List, Optional

# Define the Pydantic model for Book
class BookBase(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int

class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int

class BookResponse(BookBase):
    class Config:
        orm_mode = True  # Allow Pydantic to read data from ORM models
        from_attributes=True

class BookListResponse(BaseModel):
    books: List[BookResponse]

class MessageResponse(BaseModel):
    message: str  # Ensure the message field is defined as a string
