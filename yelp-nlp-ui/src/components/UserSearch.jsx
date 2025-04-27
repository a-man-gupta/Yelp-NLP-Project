import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';

function UserSearch() {
  const [query, setQuery] = useState('');
  const [options, setOptions] = useState([]);

  useEffect(() => {
    if (query.length > 2) {
      axios
        .get(`/api/users?query=${query}`)
        .then((res) => {
          const formatted = res.data.map((u) => ({
            value: u.user_id,
            label: `${u.name} (ID: ${u.user_id}, Reviews: ${u.review_count})`, // Include user_id and review_count
          }));
          setOptions(formatted);
        });
    }
  }, [query]);

  return (
    <div className="full-width-search">
      <Select
        options={options}
        onInputChange={(val) => setQuery(val)}
        onChange={(option) => console.log('Selected User:', option)}
        placeholder="Search Users..."
        isClearable
        isSearchable
      />
    </div>
  );
}

export default UserSearch;