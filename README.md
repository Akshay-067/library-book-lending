# Library Book Lending System

## Team Members
- AKshay
- Bhuvan
- Jashan

## Problem Statement
A department library lending application where students can browse, borrow, renew, and return books using their roll number. Librarians can add books, update copy counts, and view overdue loans. Built with React, FastAPI, and SQLite. No login is required.

## Who is doing what

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Akshay | E1, E4, E8 |  |  |  |
| Day 1 | Bhuvan | E2, E3, E5 |  |  |  |
| Day 1 | Jashan | E7, E9, E10 |  |  |  |
| Day 2 | Akshay |  |  |  |  |
| Day 2 | Bhuvan |  |  |  |  |
| Day 2 | Jashan |  |  |  |  |
| Day 3 | Akshay |  |  |  |  |
| Day 3 | Bhuvan |  |  |  |  |
| Day 3 | Jashan |  |  |  |  |

## Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| End Points | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 | GET |  |  |  ||
| E2 | GET |  |  |  ||
| E3 | POST |  |  |  ||
| E4 | PATCH |  |  |  ||
| E5 | DELETE |  |  |  ||
| E6 | POST |  |  |  ||
| E7 | PATCH |  |  |  ||
| E8 | PATCH |  |  |  ||
| E9 | GET |  |  |  ||
| E10 | GET |  |  |  ||

## Project File Organisation

```text
library-book-lending/
├── backend/
│   ├── main.py             # FastAPI app and API endpoints
│   ├── functions.py        # Supporting functions and error handling
│   ├── library.db          # SQLite database
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx
│   │   └── ...
│   ├── package.json
│   └── ...
├── docs/
│   └── team-progress.png
└── README.md
```

## API Rules

- Borrowing with **0 copies available** is rejected (`400`).
- A student cannot borrow if they already have **3 active loans** (`400`).
- A student with an overdue loan cannot borrow another book (`400`).
- A student cannot borrow a book they already have on loan (`400`).
- A loan can be renewed only once and cannot be renewed if overdue (`400`).
- A returned loan cannot be renewed or returned again (`400`).
- A book cannot be deleted while copies are out on loan (`400`).
- Total copies cannot be reduced below the number currently on loan (`400`).
- A book or loan ID that does not exist returns `404`.
- Missing or empty fields, an invalid genre, or `total_copies` outside **1–20** returns `422`.
- Borrowing decreases available copies by 1; returning increases available copies by 1.
- Each loan lasts **14 days**. Renewal adds **7 days**.
- A loan is overdue when it has not been returned and its due date is before today.

## Run Locally

**Backend**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

API docs: http://127.0.0.1:8001/docs

**Frontend** (open a second terminal)
```bash
cd frontend
npm install
npm run dev
```

