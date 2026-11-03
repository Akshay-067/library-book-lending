from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()


@app.get("/books")
def menu(genre ,title):
    return functions.get_all_books(genre =genre ,title=title)


@app.patch("/books{book_id}")
def update_total_copies(book_id:int,total_copies:int):
    return functions.update_total_copies(book_id=book_id,total_copies=total_copies)