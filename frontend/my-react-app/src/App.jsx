import { useState } from "react";
import Books from "./components/books";
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
        <h1>Library Book Lending📚</h1>
      </header>

      <section className="dashboard-section">
        <Books refreshKey={refreshKey} onChange={refreshPage} />
      </section>

      <section className="dashboard-section">
        <MyLoans refreshKey={refreshKey} onChange={refreshPage} />
      </section>

      <section className="dashboard-section">
        <Librarian refreshKey={refreshKey} onChange={refreshPage} />
      </section>
    </div>
  );
}

export default App;