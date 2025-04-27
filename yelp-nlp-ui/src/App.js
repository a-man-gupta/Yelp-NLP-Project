import React, { useState } from 'react';
import BusinessSearch from './components/BusinessSearch';
import UserSearch from './components/UserSearch';
import './App.css';

function App() {
  // State to store selected business and user
  const [selectedBusiness, setSelectedBusiness] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);

  // Handlers to update selected values
  const handleBusinessSelect = (option) => {
    setSelectedBusiness(option);
    console.log('Selected Business:', option);
  };

  const handleUserSelect = (option) => {
    setSelectedUser(option);
    console.log('Selected User:', option);
  };

  return (
    <div className="app-container">
      <div className="title">Yelp NLP Search</div>
      <div className="search-bar-container">
        <BusinessSearch onSelect={handleBusinessSelect} />
        <UserSearch onSelect={handleUserSelect} />
      </div>
      {/* Optional: Display selected values for debugging */}
      {selectedBusiness && (
        <div>Selected Business: {selectedBusiness.label}</div>
      )}
      {selectedUser && <div>Selected User: {selectedUser.label}</div>}
    </div>
  );
}

export default App;