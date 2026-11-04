from sqlalchemy import Integer, String, Boolean, Column, DateTime, create_engine, inspect, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "library.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()
print(inspect(engine).get_table_names())

class book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    total_copies = Column(Integer)
    copies_available = Column(Integer)

class loan(Base):
    __tablename__ = "Loans"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    roll_no = Column(String)
    borrowed_on = Column(DateTime, default=datetime.now)
    due_on = Column(DateTime)
    renewed = Column(Boolean)
    returned_on = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

def get_book(book_id):
    session = Session(engine)
    books = session.query(book).filter(book.id == book_id).first()
    if not books:
        session.close()
        return {"error": "Book not found", "status": 404}
    temp = {
        "id": books.id,
        "title": books.title,
        "author": books.author,
        "genre": books.genre,
        "total_copies": books.total_copies,
        "copies_available": books.copies_available,
    }
    session.close()
    return temp

def delete_book(book_id):
    session = Session(engine)
    books = session.query(book).filter(book.id == book_id)
    if not book:
        session.close()
        return None
    session.delete(book)
    session.commit()
    session.close()
    return {"book deleted"}

def add_new_book(title, author, genre, total_copies):
    session = Session(engine)
    books = book(
        title=title,
        author=author,
        genre=genre,
        total_copies=total_copies,
        copies_available=total_copies
    )
    session.add(book)
    session.commit()
    session.refresh(book)
    
    temp = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "total_copies": book.total_copies,
        "copies_available": book.copies_available
    }
    session.close()
    return temp