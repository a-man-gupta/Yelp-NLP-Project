import React, { useState } from 'react';
import './GenerateReview.css';

function GenerateReview({ businessId, userId }) {
  const [helpfulText, setHelpfulText] = useState('');
  const [generatedReview, setGeneratedReview] = useState(null);
  const [error, setError] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerateReviewSubmit = async (e) => {
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
    if (!helpfulText.trim()) {
      setError('Please enter helpful text.');
      return;
    }

    setIsGenerating(true);

    try {
      const response = await fetch('/api/generate-review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ business_id: businessId, user_id: userId, helpful_text: helpfulText }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Failed to generate review');
      }

      setGeneratedReview(data.generated_review);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="generate-review-container">
      <div className="generate-review-row">
        <div className="review-form-container">
          <form onSubmit={handleGenerateReviewSubmit} className="review-form">
            <textarea
              value={helpfulText}
              onChange={(e) => setHelpfulText(e.target.value)}
              placeholder="Enter helpful text for review generation..."
              className="review-textarea"
              rows="4"
            />
            <button type="submit" className="submit-button" disabled={isGenerating}>
              {isGenerating ? 'Generating...' : 'Generate Review'}
            </button>
          </form>
          {error && <div className="error-message">{error}</div>}
        </div>
        {generatedReview && (
          <div className="generated-review-container">
            <div className="generated-review-text">{generatedReview}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default GenerateReview;