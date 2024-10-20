from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base, engine
from auth.dependencies import get_db
from sqlalchemy.orm import Session
from log.custom_logger import setup_logger

logger = setup_logger('log/lib_mang')

# Define the Book model (SQLAlchemy)
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    publication_year = Column(Integer, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Function to add a book
def add_book(book: Book, db: Session):
    db_book = Book(**book.dict())  # Create a Book instance from the Pydantic model
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    logger.info('Book added successfully: %s', db_book.title)
    return db_book

# Function to display all books
def display_books(db: Session):
    books = db.query(Book).all()
    return books

# Function to search a book by ID
def search_book_by_id(book_id: int, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()
    return book

# Function to search multiple books by their IDs
def search_books_by_ids(book_ids: list, db: Session):
    books = db.query(Book).filter(Book.id.in_(book_ids)).all()
    return books

# Function to update a book by ID
def update_book_by_id(book_id: int, book: Book, db: Session):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        return {"error": "Book not found."}
    
    # Update only the fields provided in the request
    if book.title:
        db_book.title = book.title
    if book.author:
        db_book.author = book.author
    if book.publication_year:
        db_book.publication_year = book.publication_year
    
    db.commit()
    logger.info('Book updated: %s', db_book.title)
    return db_book  # Return the updated book instance

# Function to delete a book by ID
def delete_book_by_id(book_id: int, db: Session):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {"error": "Book not found."}
    
    db.delete(book)
    db.commit()
    logger.info('Book deleted: %s', book.title)
    return {"message": "Book deleted successfully."}
