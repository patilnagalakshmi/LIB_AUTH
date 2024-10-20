from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import security
from auth.routes import auth_router
from users.routes import users_router
from service import add_book, display_books, search_book_by_id, search_books_by_ids, update_book_by_id, delete_book_by_id
from pydantic_model import BookCreate, BookResponse, BookListResponse, MessageResponse
from auth.dependencies import get_db,oauth2_scheme
from auth.dependencies import get_current_user, get_db
from users.usermodel import User
from typing import List

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LIBRARY MANAGEMENT!!!"}

# POST: Create a new book
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    created_book = add_book(book, db)
    return BookResponse.from_orm(created_book)  # Ensure to return the Pydantic response model

# GET: Get all books
@app.get("/books/all", response_model=BookListResponse)
def get_all_books(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    books = display_books(db)
    return BookListResponse(books=[BookResponse.from_orm(book) for book in books]) if books else {"message": "No books found."}

# GET: Get a single book by ID
@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    book = search_book_by_id(book_id, db)
    if book:
        return BookResponse.from_orm(book)
    else:
        raise HTTPException(status_code=404, detail="Book not found.")

# GET: Get books by multiple IDs
@app.get("/books/multiple", response_model=List[BookResponse])
def get_books_by_ids(book_ids: str, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    book_ids_list = [int(id.strip()) for id in book_ids.split(',')]
    books = search_books_by_ids(book_ids_list, db)
    return [BookResponse.from_orm(book) for book in books] if books else HTTPException(status_code=404, detail="No books found for the given IDs.")

# PUT: Update a book by ID
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    updated_book = update_book_by_id(book_id, book, db)
    
    # Check if the updated_book is None, indicating that the book was not found
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Return the updated book response
    return BookResponse.from_orm(updated_book)

# DELETE: Delete a book by ID
@app.delete("/books/{book_id}", response_model=MessageResponse)
def delete_book(book_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    result = delete_book_by_id(book_id, db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
