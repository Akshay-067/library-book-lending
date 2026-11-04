from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions    

app = FastAPI()

@app.get("/books/{book_id}")
def get_book(book_id: int):
    return functions.get_book(book_id = book_id)

@app.post("/books")
def add_book(title: str, author: str, total_copies: int, genre: str, copies_available: int):
    return functions.add_book(title=title, author=author, total_copies=total_copies, genre=genre, copies_available=copies_available)

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    return functions.delete_book(book_id=book_id)



@app.get("/books")
def menu(genre ,title):
    return functions.get_all_books(genre =genre ,title=title)


@app.patch("/books{book_id}")
def update_total_copies(book_id:int,total_copies:int):
    return functions.update_total_copies(book_id=book_id,total_copies=total_copies)
