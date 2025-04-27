import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './PredictRatings.css';

function PredictRatings({ businessId, userId }) {
  const [reviewText, setReviewText] = useState('');
  const [ratings, setRatings] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Validate inputs
    if (!businessId) {
      setError('Please select a business.');
      return;
    }
    if (!userId) {
      setError('Please select a user.');
      return;
    }
    if (!reviewText.trim()) {
      setError('Please enter review text.');
      return;
    }

    setIsLoading(true);

    try {
      console.log('Sending API request with:', { business_id: businessId, user_id: userId, review_text: reviewText });
      const response = await fetch('/api/predict-ratings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ business_id: businessId, user_id: userId, review_text: reviewText }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch ratings');
      }

      console.log('API response:', data);
      setRatings(data.ratings);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Prepare data for histograms
  const chartData = ratings
    ? [
        { name: 'Funny', value: ratings.funny },
        { name: 'Useful', value: ratings.useful },
        { name: 'Cool', value: ratings.cool },
      ]
    : [];

  return (
    <div className="predict-ratings-container">
      <form onSubmit={handleSubmit} className="review-form">
        <textarea
          value={reviewText}
          onChange={(e) => setReviewText(e.target.value)}
          placeholder="Enter your review text here..."
          className="review-textarea"
          rows="4"
        />
        <button type="submit" className="submit-button" disabled={isLoading}>
          {isLoading ? 'Submitting...' : 'Predict Ratings'}
        </button>
      </form>
      {error && <div className="error-message">{error}</div>}
      {ratings && (
        <div className="ratings-charts">
          <h3>Predicted Ratings</h3>
          <div className="charts-container">
            {chartData.map((data, index) => (
              <div className="chart" key={data.name}>
                <h4>{data.name}</h4>
                <ResponsiveContainer width="100%" height={100}>
                  <BarChart data={[data]} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 5]} ticks={[0, 1, 2, 3, 4, 5]} />
                    <Tooltip />
                    <Bar
                      dataKey="value"
                      fill={index === 0 ? '#ff6b6b' : index === 1 ? '#4ecdc4' : '#45b7d1'}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default PredictRatings;