import React, { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const apiBaseUrl =
        // import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
        import.meta.env.VITE_API_BASE_URL ||
        "https://next-builder-api.onrender.com";
      const response = await fetch(
        `${apiBaseUrl}/search?q=${encodeURIComponent(query)}`,
      );
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1 className="logo">
          Next <span>Construction Solutions</span>
        </h1>
        <p className="subtitle">
          One search for every spec, safety log, invoice, and regulation you
          need.
        </p>
      </header>

      <main>
        <form onSubmit={handleSearch} className="search-form">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search specs, logs, or procedures..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="search-input"
            />
            <button type="submit" className="search-button">
              {loading ? <div className="spinner"></div> : "Search"}
            </button>
          </div>
        </form>

        <div className="results-container">
          {results.length > 0
            ? results.map((res) => (
                <div key={res.id} className="result-card">
                  <div className="result-header">
                    <span className="doc-type">{res.type}</span>
                    <span className="doc-score">Score: {res.score}</span>
                  </div>
                  <p>{res.content}</p>
                </div>
              ))
            : !loading &&
              query && (
                <p className="no-results">No relevant documents found.</p>
              )}
        </div>
      </main>
    </div>
  );
}

export default App;
