import React, { useState } from 'react';
import BusinessSearch from './components/BusinessSearch';

function App() {
  const [selectedBusiness, setSelectedBusiness] = useState(null);

  return (
    <div>
      <h1>Yelp NLP Project</h1>
      <BusinessSearch onSelect={setSelectedBusiness} />
      {selectedBusiness && (
        <div>
          <h2>Selected Business:</h2>
          <p>{selectedBusiness.name} – {selectedBusiness.address}</p>
        </div>
      )}
    </div>
  );
}

export default App;

// import React from 'react'; 
// $env:NODE_OPTIONS="--openssl-legacy-provider"