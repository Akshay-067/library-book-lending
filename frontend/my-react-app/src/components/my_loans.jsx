import { useState, useEffect } from "react";
import { API_URL } from "../api";

function MyLoans({ refreshKey, onChange }) {
    const [rollNo, setRollNo] = useState("");
    const [shownRoll, setShownRoll] = useState("");
    const [loans, setLoans] = useState([]);
    const [message, setMessage] = useState("");

    function showLoans() {
        fetch(`${API_URL}/loans/student/${shownRoll}`)
            .then((response) => {
                return response.json().then((data) => ({ response, data }));
            })
            .then(({ response, data }) => {
                if (response.ok) {
                    setLoans(data);
                    if (data.length === 0) {
                        setMessage("No loans found for this roll number");
                    } else {
                        setMessage("");
                    }
                } else {
                    setLoans([]);
                    setMessage(data.detail);
                }
            });
    }

    useEffect(() => {
        if (shownRoll !== "") {
            showLoans();
        }
    }, [shownRoll, refreshKey]);

    function renewLoan(id) {
        fetch(`${API_URL}/loans/${id}/renew`, { method: "PATCH" })
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

    function returnLoan(id) {
        fetch(`${API_URL}/loans/${id}/return`, { method: "PATCH" })
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
            <h2>My Loans</h2>

            <p className="error">{message}</p>

            <input
                placeholder="Enter Roll Number"
                value={rollNo}
                onChange={(e) => setRollNo(e.target.value)}
            />
            <button onClick={() => setShownRoll(rollNo)}>
                Show
            </button>

            {loans.map((loan) => (
                <div key={loan.id} className="book-card">
                    <h3>{loan.title}</h3>
                    <p>Due: {loan.due_on.slice(0, 10)}</p>
                    {new Date(loan.due_on) < new Date() && <p>Overdue</p>}

                    <button onClick={() => renewLoan(loan.id)}>Renew</button>
                    <button onClick={() => returnLoan(loan.id)}>Return</button>
                </div>
            ))}
        </div>
    );
}

export default MyLoans;