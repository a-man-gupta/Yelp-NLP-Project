import { useState, useEffect } from 'react';
import axios from 'axios';
import React from 'react';


function BusinessSearch({ onSelect }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      if (query.length > 1) {
        axios.get(`/api/businesses?query=${query}`).then(res => {
          setResults(res.data);
        });
      }
    }, 300);

    return () => clearTimeout(delayDebounce);
  }, [query]);

  return (
    <div>
      <input
        placeholder="Search business"
        value={query}
        onChange={e => setQuery(e.target.value)}
      />
      <ul>
        {results.map(b => (
          <li key={b.business_id} onClick={() => onSelect(b)}>
            {b.name} – {b.address}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BusinessSearch;
