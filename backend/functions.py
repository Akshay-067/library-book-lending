from sqlalchemy import Integer, String, Column, DateTime, create_engine, inspect, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime
DB_PATH = "library.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()
print(inspect(engine).get_table_names())

class book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(str)
    author = Column(str)
    genre = Column(String)
    total_copies = Column(int)
    copies_available = Column(int)

class Update(Base):
    __tablename__ = "updates"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    roll_no = Column(String)
    borrowed_on = Column(DateTime, default=datetime.now)
    due_on = Column(DateTime)
    renewed = Column(bool)
    returned_on = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

def get_all_books():
    session = Session(engine)
    books = session.query(book).all()
    response = []
    for book in books:
        temp_books = {
            "id" : books.id,
            "title" : books.title,
            "author" : books.author,
            "genre" : books.genre,
            "total_copies" : books.total_copies,
            "copies_available":books.copies_available,
        }
        response.append(temp_books)
    session.close()
    return response

def update_total_copies(book_id, new_total_copies):
    session = Session(engine)
    books = session.query(book).filter(book.id == book_id)
    diff = new_total_copies - book.total_copies
    book.total_copies = new_total_copies
    book.copies_available = book.copies_available + diff
    session.commit()

    temp = {
        "id": books.id,
        "title": books.title,
        "author": books.author,
        "genre": books.genre,
        "total_copies": books.total_copies,
        "copies_available": books.copies_available
    }
    session.close()
    return temp
