from sqlalchemy import Integer, String, Column, create_engine, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime

DB_PATH = "library.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Update(Base):
    __tablename__ = "updates"
    id = Column(Integer, foreign_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    roll_no = Column(String)
    borrowed_on = Column(DateTime, default=datetime.now)
    due_on = Column(DateTime)
    renewed = Column(Boolean)
    returned_on = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)