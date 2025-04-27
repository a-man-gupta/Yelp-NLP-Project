import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Select from 'react-select';

function BusinessSearch({ onSelect }) {
  const [query, setQuery] = useState('');
  const [options, setOptions] = useState([]);

  useEffect(() => {
    if (query.length > 2) {
      axios
        .get(`/api/businesses?query=${query}`)
        .then((res) => {
          const formatted = res.data.map((b) => ({
            value: b.business_id,
            label: `${b.name} - ${b.address}`,
          }));
          setOptions(formatted);
        })
        .catch((err) => console.error('Business search error:', err));
    }
  }, [query]);

  return (
    <div className="full-width-search">
      <Select
        options={options}
        onInputChange={(val) => setQuery(val)}
        onChange={(option) => {
          console.log('BusinessSearch selected:', option); // Keep for debugging
          onSelect(option); // Call the onSelect prop
        }}
        placeholder="Search Businesses..."
        isClearable
        isSearchable
      />
    </div>
  );
}

export default BusinessSearch;