from sqlalchemy import Integer, String, Boolean, Column, DateTime, create_engine, inspect, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime,timedelta,timezone
import jwt 
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph=PasswordHasher()
DB_PATH = "library.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRY=7*24*60
SECRET_KEY ="SECRET067"
ALGORITHM = "HS256"


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

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    password = Column(String)


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
    if books is None:
        session.close()
        return None

    if new_total_copies < books.total_copies - books.copies_available:
        session.close()
        return "below_loans"
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
        return None  
    if loan.returned_on:
        session.close()
        return "already_returned"  

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

def loan_renewal(loan_id: int):
    session = Session(engine)
    loan = session.query(loans).filter(loans.id == loan_id).first()
    result = None
    if loan is None:
        result = None
    elif loan.returned_on is not None:
        result = "already_returned"
    elif loan.renewed:
        result = "already_renewed"
    elif loan.due_on < datetime.today():
        result = "overdue"
    else:
        loan.due_on = loan.due_on + timedelta(days=7)
        loan.renewed = True
        session.commit()
        result = {"id": loan_id, "due_on": loan.due_on}
    session.close()
    return result


def loans_overdue():
    session = Session(engine)
    active_loans = session.query(loans).filter(loans.returned_on.is_(None)).all()
    response = []
    for loan in active_loans:
        if loan.due_on and loan.due_on < datetime.today():
            books = session.query(book).filter(book.id == loan.book_id).first()
            response.append({
                "id": loan.id,
                "book_id": loan.book_id,
                "title": books.title,
                "roll_no": loan.roll_no,
                "due_on": loan.due_on
            })
            
    session.close()
    return response


def student_loans(roll_no: str):
    session = Session(engine)

    active_loans = session.query(loans).filter(
        loans.roll_no == roll_no,
        loans.returned_on.is_(None)
    ).all()

    response = []
    for loan in active_loans:
        books = session.query(book).filter(book.id == loan.book_id).first() 
        response.append({
            "id": loan.id,
            "book_id": loan.book_id,
            "title": books.title,
            "due_on": loan.due_on
        })
    session.close()
    return response

def get_book(book_id):
    session = Session(engine)
    books = session.query(book).filter(book.id == book_id).first() 
    if not books:
        session.close()
        return None
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
    books = session.query(book).filter(book.id == book_id).first()  
    if not books:
        session.close()
        return None
    if books.copies_available < books.total_copies:
        session.close()
        return "on_loan"
    session.delete(books)
    session.commit()
    session.close()
    return {"message": "book deleted"}

def add_new_book(title, author, genre, total_copies):
    session = Session(engine)
    books = book(
        title=title,
        author=author,
        genre=genre,
        total_copies=total_copies,
        copies_available=total_copies
    )
    session.add(books)
    session.commit()
    session.refresh(books)
    
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


def borrow_book(book_id, roll_no):
    session = Session(engine)
    books = session.query(book).filter(book.id == book_id).first()
    if not books:
        session.close()
        return None
    if books.copies_available == 0:
        session.close()
        return "no_copies"

    active = session.query(loans).filter(
        loans.roll_no == roll_no,
        loans.returned_on.is_(None)
    ).all()
    if len(active) >= 3:
        session.close()
        return "max_loans"
    for loan in active:
        if loan.due_on < datetime.today():
            session.close()
            return "has_overdue"
    for loan in active:
        if loan.book_id == book_id:
            session.close()
            return "already_has"

    new_loan = loans(
        book_id=book_id,
        roll_no=roll_no,
        borrowed_on=datetime.today(),
        due_on=datetime.today() + timedelta(days=14),
        renewed=False
    )
    books.copies_available -= 1
    session.add(new_loan)
    session.commit()
    session.refresh(new_loan)
    temp = {"id": new_loan.id, "book_id": book_id, "roll_no": roll_no, "due_on": new_loan.due_on}
    session.close()
    return temp


def verify_login(username, password):
    session=Session(engine)
    user=session.query(User).filter_by(user_name=username).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.password,password)
    except VerifyMismatchError:
        session.close()
        return False
    session.close()
    access_token=create_token(username=username,token_type="access")
    refresh_token=create_token(username=username,token_type="refresh")
    return {"access_token":access_token,"refresh_token":refresh_token}
        
    
    
def create_token(username,token_type):
    time=ACCESS_TOKEN_EXPIRE_MINUTES
    if token_type == "refresh":
        time=REFRESH_TOKEN_EXPIRY
    payload = {
        "username": username,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)

    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token( token, token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return False   
    if payload["token_type"] == token_type:
        return payload["username"]
    return False

def register_user(user_name:str,password:str):
    session = Session(engine)
    user_exists=session.query(User).filter_by(user_name=user_name).first()
    if user_exists is not None:
        session.close()
        return False
    session.add(User(user_name=user_name,password=ph.hash(password)))
    session.commit()
    session.close()
    return True
