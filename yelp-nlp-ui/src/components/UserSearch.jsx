import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';

function UserSearch({ onSelect }) {
  const [query, setQuery] = useState('');
  const [options, setOptions] = useState([]);

  useEffect(() => {
    if (query.length > 2) {
      axios
        .get(`/api/users?query=${query}`)
        .then((res) => {
          const formatted = res.data.map((u) => ({
            value: u.user_id,
            label: `${u.name} (ID: ${u.user_id}, Reviews: ${u.review_count})`,
          }));
          setOptions(formatted);
        })
        .catch((err) => console.error('User search error:', err));
    }
  }, [query]);

  return (
    <div className="full-width-search">
      <Select
        options={options}
        onInputChange={(val) => setQuery(val)}
        onChange={(option) => {
          console.log('UserSearch selected:', option); // Keep for debugging
          onSelect(option); // Call the onSelect prop
        }}
        placeholder="Search Users..."
        isClearable
        isSearchable
      />
    </div>
  );
}

export default UserSearch;