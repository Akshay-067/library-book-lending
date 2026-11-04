from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions    

app = FastAPI()

@app.get("/books/{book_id}")
def get_book(book_id: int):
    results=functions.get_book(book_id = book_id)
    if not results:
        raise HTTPException(status_code=404, detail="Book not found")
    return results


@app.post("/books")
def add_book(title: str, author: str, total_copies: int, genre: str):
    return functions.add_new_book(title=title, author=author, total_copies=total_copies, genre=genre)

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    return functions.delete_book(book_id=book_id)

@app.get("/books")
def menu(genre: str = None, title: str = None):
    return functions.get_all_books(genre=genre, title=title)


@app.patch("/books/{book_id}")
def update_total_copies(book_id:int,total_copies:int):
    return functions.update_total_copies(book_id=book_id,new_total_copies=total_copies)

@app.patch("/loans/{loan_id}/return")
def return_loan(loan_id: int):
    return functions.loan_return(loan_id)

@app.patch("/loans/{loan_id}/renew")
def loan_renew(loan_id: int):
    return functions.loan_renewal(loan_id)

@app.get("/loans/student/{roll_no}")
def loan_student(roll_no: str):
    return functions.student_loans(roll_no)


@app.get("/loans/overdue")
def overdue():
    return functions.loans_overdue()