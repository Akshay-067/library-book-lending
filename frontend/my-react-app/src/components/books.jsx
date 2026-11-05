import React, { useState, useEffect } from "react";

function Books({ refreshKey, onChange }) {

    const [books, setBooks] = useState([]);
    const [search, setSearch] = useState("");
    const [genre, setGenre] = useState("");
    const [rollNo, setRollNo] = useState("");

    const API_URL = "http://127.0.0.1:8001";

    function getBooks() {
        fetch(`${API_URL}/books`)
            .then((response) => response.json())
            .then((data) => {
                setBooks(data);
            });
    }

    useEffect(() => {
        getBooks();
    }, [refreshKey]);

    function borrowBook(id) {

        if (rollNo === "") {
            alert("Enter your roll number");
            return;
        }

        fetch(`${API_URL}/loans?book_id=${id}&roll_no=${rollNo}`, { method: "POST" })
            .then((response) => {
                return response.json().then((data) => ({ response, data }));
            })
            .then(({ response, data }) => {
                if (!response.ok) {
                    alert(data.detail);
                    return;
                }

                alert("Book borrowed successfully!");

                setRollNo("");
                onChange();
            });
    }

    const filteredBooks = books.filter((book) => {
        return (
            book.title.includes(search) &&
            (genre === "" || book.genre === genre)
        );
    });

    function showDetails(id) {

        fetch(`${API_URL}/books/${id}`)
            .then((response) => response.json())
            .then((book) => {
                alert(
                    "Title: " + book.title +
                    "\nAuthor: " + book.author +
                    "\nGenre: " + book.genre +
                    "\nAvailable Copies: " + book.copies_available
                );
            });
    }

    return (
        <div>

            <h2>Library Books</h2>

            <input
                type="text"
                placeholder="Search books"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            />

            <select
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
            >
                <option value="">All Genres</option>
                <option value="textbook">Textbook</option>
                <option value="fiction">Fiction</option>
                <option value="reference">Reference</option>
                <option value="magazine">Magazine</option>
                <option value="biography">Biography</option>
            </select>

            <input
                type="text"
                placeholder="Enter Roll Number"
                value={rollNo}
                onChange={(e) => setRollNo(e.target.value)}
            />

            {filteredBooks.map((book) => (

                <div className="book-card" key={book.id}>

                    <h3>{book.title}</h3>

                    <p>Author: {book.author}</p>
                    <p>Genre: {book.genre}</p>
                    <p>Available Copies: {book.copies_available}</p>

                    {book.copies_available === 0 ? (
                        <p>Not Available</p>
                    ) : (
                        <button onClick={() => borrowBook(book.id)}>
                            Borrow
                        </button>
                    )}

                    <button onClick={() => showDetails(book.id)}>
                        View Details
                    </button>

                </div>

            ))}

        </div>
    );
}

export default Books;