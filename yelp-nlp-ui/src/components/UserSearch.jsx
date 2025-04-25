import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Tile from './Tile';

function UserSearch({ onSelect }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [page, setPage] = useState(1);

  useEffect(() => {
    if (query.length > 1) {
      axios
        .get(`/api/users?query=${query}&page=${page}&limit=5`)
        .then(res => setResults(res.data));
    } else {
      setResults([]);
    }
  }, [query, page]);

  return (
    <div className="search-panel">
      <input
        className="search-bar"
        placeholder="Search users..."
        value={query}
        onChange={e => {
          setQuery(e.target.value);
          setPage(1); // reset page
        }}
      />
      <div className="tile-container">
        {results.map(u => (
          <Tile key={u.user_id} item={u} onClick={onSelect} isBusiness={false} />
        ))}
      </div>
      {results.length > 0 && (
        <div className="pagination">
          <button onClick={() => setPage(p => Math.max(1, p - 1))}>Prev</button>
          <span>Page {page}</span>
          <button onClick={() => setPage(p => p + 1)}>Next</button>
        </div>
      )}
    </div>
  );
}

export default UserSearch;
