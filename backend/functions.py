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

def get_all_books():
    session = Session(engine)
    books = session.query(book).all()
    response = []
    for b in books:
        temp_books = {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "genre": b.genre,
            "total_copies": b.total_copies,
            "copies_available": b.copies_available,
        }
        response.append(temp_books)
    session.close()
    return response

def update_total_copies(book_id, new_total_copies):
    session = Session(engine)
    b = session.query(book).filter(book.id == book_id).first()
    diff = new_total_copies - b.total_copies
    b.total_copies = new_total_copies
    b.copies_available = b.copies_available + diff
    session.commit()

    temp = {
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "genre": b.genre,
        "total_copies": b.total_copies,
        "copies_available": b.copies_available,
    }
    session.close()
    return temp