import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTranslate = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    setResult(null);
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
      });

      if (!response.ok) {
        throw new Error('Something went wrong with the server.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleCopyToClipboard = () => {
    if (result && result.command) {
        navigator.clipboard.writeText(result.command)
          .then(() => alert('Command copied to clipboard!'))
          .catch(err => console.error('Failed to copy: ', err));
    }
  };

  return (
    <div className="container">
      <header>
        <h1>GitLingo 🧠</h1>
        <p>Translate plain English to Git commands using AI.</p>
      </header>

      <div className="search-box">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., 'save my work without committing'"
          onKeyPress={(e) => e.key === 'Enter' && handleTranslate()}
        />
        <button onClick={handleTranslate} disabled={isLoading}>
          {isLoading ? 'Translating...' : 'Translate'}
        </button>
      </div>

      <div className="result-box">
        {error && <div className="error">{error}</div>}
        {result && (
            <div className="result-card">
              <h3>Suggested Command:</h3>
              <div className="command-display">
                <code>{result.command}</code>
                <button className="copy-btn" onClick={handleCopyToClipboard}>Copy</button>
              </div>
              <p>{result.description}</p>
            </div>
        )}
      </div>
    </div>
  );
}

export default App;
