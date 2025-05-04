import React, { useState, useEffect } from 'react';
import BusinessSearch from './components/BusinessSearch';
import UserSearch from './components/UserSearch';
import PredictRatings from './components/PredictRatings';
import GenerateReview from './components/GenerateReview';
import './App.css';

function App() {
  const [selectedBusiness, setSelectedBusiness] = useState(null);
  const [selectedUser, setSelectedUser] = useState(null);

  const handleBusinessSelect = (option) => {
    console.log('handleBusinessSelect called with:', option);
    setSelectedBusiness(option);
  };

  const handleUserSelect = (option) => {
    console.log('handleUserSelect called with:', option);
    setSelectedUser(option);
  };

  // Debug: Log state changes
  useEffect(() => {
    console.log('State updated:', { selectedBusiness, selectedUser });
    console.log('Passing to PredictRatings:', {
      businessId: selectedBusiness?.value,
      userId: selectedUser?.value,
    });
  }, [selectedBusiness, selectedUser]);

  return (
    <div className="app-container">
      <div className="title">Yelp NLP Challenge - The Best One</div>
      <div className="search-bar-container">
        <BusinessSearch onSelect={handleBusinessSelect} />
        <UserSearch onSelect={handleUserSelect} />
      </div>
      <div className="predict-ratings-wrapper">
        <PredictRatings
          businessId={selectedBusiness?.value} // Correct: value contains business_id
          userId={selectedUser?.value} // Correct: value contains user_id
        />
      </div>
      <div className="generate-review-wrapper">
        <GenerateReview
          businessId={selectedBusiness?.value}
          userId={selectedUser?.value}
        />
      </div>
    </div>
  );
}

export default App;

// $env:NODE_OPTIONS="--openssl-legacy-provider"