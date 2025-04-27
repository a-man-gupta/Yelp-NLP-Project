import React from 'react';
import BusinessSearch from './components/BusinessSearch';
import UserSearch from './components/UserSearch';
import './App.css';

function App() {
  return (
    <div className="app-container">
      <div className="title">Yelp NLP Search</div>
      <div className="search-bar-container">
        <BusinessSearch />
        <UserSearch />
      </div>
    </div>
  );
}

export default App;
