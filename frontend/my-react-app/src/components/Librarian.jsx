import { useState, useEffect } from "react";
import { API_URL } from "../api";

const GENRES = ["textbook", "fiction", "reference", "magazine", "biography"];

function Librarian({ refreshKey, onChange }) {
    const [books, setBooks] = useState([]);
    const [overdue, setOverdue] = useState([]);
    const [copies, setCopies] = useState({});
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [genre, setGenre] = useState("textbook");
    const [total, setTotal] = useState("");
    const [message, setMessage] = useState("");

    function loadData() {
        fetch(`${API_URL}/books`)
            .then((response) => response.json())
            .then((data) => setBooks(data));

        fetch(`${API_URL}/loans/overdue`)
            .then((response) => response.json())
            .then((data) => setOverdue(data));
    }

    useEffect(() => {
        loadData();
    }, [refreshKey]);

    function addBook() {
        fetch(`${API_URL}/books?title=${title}&author=${author}&genre=${genre}&total_copies=${total}`, { method: "POST" })
            .then((response) => {
                return response.json().then((data) => ({ response, data }));
            })
            .then(({ response, data }) => {
                if (response.ok) {
                    setMessage("");
                    setTitle("");
                    setAuthor("");
                    setTotal("");
                    onChange();
                } else {
                    setMessage(data.detail);
                }
            });
    }

    function saveCopies(id) {
        fetch(`${API_URL}/books/${id}?total_copies=${copies[id]}`, { method: "PATCH" })
            .then((response) => {
                return response.json().then((data) => ({ response, data }));
            })
            .then(({ response, data }) => {
                if (response.ok) {
                    setMessage("");
                    onChange();
                } else {
                    setMessage(data.detail);
                }
            });
    }

    function deleteBook(id) {
        fetch(`${API_URL}/books/${id}`, { method: "DELETE" })
            .then((response) => {
                return response.json().then((data) => ({ response, data }));
            })
            .then(({ response, data }) => {
                if (response.ok) {
                    setMessage("");
                    onChange();
                } else {
                    setMessage(data.detail);
                }
            });
    }

    return (
        <div>
            <h2>Librarian</h2>

            <p className="error">{message}</p>

            <h3>Overdue loans</h3>
            {overdue.map((loan) => (
                <p key={loan.id}>
                    {loan.title} - {loan.roll_no}
                </p>
            ))}

            <h3>Add a book</h3>
            <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
            <input placeholder="Author" value={author} onChange={(e) => setAuthor(e.target.value)} />
            <select value={genre} onChange={(e) => setGenre(e.target.value)}>
                {GENRES.map((g) => (
                    <option key={g} value={g}>{g}</option>
                ))}
            </select>
            <input placeholder="Total copies" type="number" value={total} onChange={(e) => setTotal(e.target.value)} />
            <button onClick={addBook}>Add</button>

            <h3>Books</h3>
            {books.map((book) => (
                <div key={book.id}>
                    <span>{book.title} ({book.copies_available}/{book.total_copies}) </span>
                    <input
                        type="number"
                        value={copies[book.id] || book.total_copies}
                        onChange={(e) => setCopies({ ...copies, [book.id]: e.target.value })}
                    />
                    <button onClick={() => saveCopies(book.id)}>Save</button>
                    <button onClick={() => deleteBook(book.id)}>Delete</button>
                </div>
            ))}
        </div>
    );
}

export default Librarian;