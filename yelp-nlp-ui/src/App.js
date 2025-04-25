import React, { useState } from 'react';
import BusinessSearch from './components/BusinessSearch';
import UserSearch from './components/UserSearch';
import './App.css';

function App() {
  const [selectedItem, setSelectedItem] = useState(null);

  return (
    <div className="app-container">
      <div className="title">Yelp NLP Search</div>
      <div className="split-screen">
        <div className="left-pane">
          <h2>Businesses</h2>
          <BusinessSearch onSelect={setSelectedItem} />
        </div>
        <div className="right-pane">
          <h2>Users</h2>
          <UserSearch onSelect={setSelectedItem} />
        </div>
      </div>
      {selectedItem && (
        <div className="selected-tile">
          <h3>Selected: {selectedItem.name}</h3>
          {'address' in selectedItem && <p>{selectedItem.address}</p>}
          {'review_count' in selectedItem && <p>Review Count: {selectedItem.review_count}</p>}
        </div>
      )}
    </div>
  );
}

export default App;
