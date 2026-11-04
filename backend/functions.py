from sqlalchemy import Integer, String, Boolean, Column, DateTime, create_engine, inspect, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime,timedelta

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

class loans(Base):
    __tablename__ = "Loans"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    roll_no = Column(String)
    borrowed_on = Column(DateTime, default=datetime.now)
    due_on = Column(DateTime)
    renewed = Column(Boolean)
    returned_on = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

def get_all_books(genre=None, title=None):
    session = Session(engine)
    query = session.query(book)
    if genre:
        query = query.filter(book.genre == genre)
    if title:
        query = query.filter(book.title.contains(title))
    books = query.all()
    response = []
    for books in books:
        temp_books = {
            "id": books.id,
            "title": books.title,
            "author": books.author,
            "genre": books.genre,
            "total_copies": books.total_copies,
            "copies_available": books.copies_available,
        }
        response.append(temp_books)
    session.close()
    return response

def update_total_copies(book_id, new_total_copies):
    session = Session(engine)
    books = session.query(book).filter(book.id == book_id).first()
    diff = new_total_copies - books.total_copies
    books.total_copies = new_total_copies
    books.copies_available = books.copies_available + diff
    session.commit()

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


def loan_return(loan_id: int):
    session = Session(engine)
    loan = session.query(loans).filter(loans.id == loan_id).first()

    if not loan:
        session.close()
        return {"error": "Loan not found", "status": 404}
    if loan.returned_on:
        session.close()
        return {"error": "Loan already returned", "status": 400}

    loan.returned_on = datetime.today()

    books = session.query(book).filter(book.id == loan.book_id).first()
    if books:
        books.copies_available += 1

    session.commit()

    temp = {
        "id": loan.id,
        "book_id": loan.book_id,
        "roll_no": loan.roll_no,
        "returned_on": loan.returned_on
    }
    session.close()
    return temp