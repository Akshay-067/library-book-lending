import { useState } from "react";

import books from "./components/books";
import Librarian from "./components/Librarian";
import MyLoans from "./components/my_loans";


function App() {
  const [refreshKey, setRefreshKey] = useState(0);

  function refreshPage() {
    setRefreshKey(refreshKey + 1);
  }

  return (
    <div className="app-container">
      <header className="page-header">
        <h1> Library Book Lending </h1>
        <p>Borrow and return books from the library
            (you will not read it anyways).</p>
      </header>

      <section className="dashboard-section">
        <Librarian refreshKey={refreshKey} />
      </section>

      <section className="dashboard-section">
        <my_loans />
      </section>

      <section className="dashboard-section">
        <my_loans onLoanAdded={refreshPage} />
      </section>
    </div>
  );
}

export default App;