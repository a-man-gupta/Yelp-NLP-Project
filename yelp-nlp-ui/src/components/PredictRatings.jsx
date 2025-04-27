import React, { useState } from 'react';
import { RadialBarChart, RadialBar, ResponsiveContainer, PolarAngleAxis } from 'recharts';
import './PredictRatings.css';

function PredictRatings({ businessId, userId }) {
  const [reviewText, setReviewText] = useState('');
  const [ratings, setRatings] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

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

  // Prepare data for radial charts
  const chartData = ratings
    ? [
        { name: 'Funny', value: ratings.funny, fill: '#ff6b6b' },
        { name: 'Useful', value: ratings.useful, fill: '#4ecdc4' },
        { name: 'Cool', value: ratings.cool, fill: '#45b7d1' },
      ]
    : [];

  return (
    <div className="predict-ratings-container">
      <div className="predict-ratings-row">
        <div className="review-form-container">
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
        </div>
        {ratings && (
          <div className="ratings-charts">
            <div className="charts-container">
              {chartData.map((data, index) => (
                <div className="chart" key={data.name}>
                  <h4>{data.name}: {data.value}</h4>
                  <ResponsiveContainer width="100%" height={120}>
                    <RadialBarChart
                      innerRadius="20%"
                      outerRadius="80%"
                      data={[{ ...data, value: (data.value / 5) * 100 }]}
                      startAngle={90}
                      endAngle={-270}
                    >
                      <RadialBar
                        minAngle={15}
                        background
                        clockWise
                        dataKey="value"
                        fill={data.fill}
                      />
                      <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
                    </RadialBarChart>
                  </ResponsiveContainer>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PredictRatings;