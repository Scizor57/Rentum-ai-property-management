import React from 'react';

const AIReviews = ({ 
  currentUser,
  filteredData,
  reviewRequestForm,
  setReviewRequestForm,
  handleReviewRequest,
  reviewResponseForm,
  setReviewResponseForm,
  handleReviewResponse 
}) => {
  return (
    <div className="section">
      <h2>🤖 AI-Powered Review System</h2>
      <div className="reviews-container">
        
        {/* Review Request Section */}
        <div className="review-section">
          <h3>📝 Request Review</h3>
          <div className="form">
            <select 
              value={reviewRequestForm.request_type} 
              onChange={(e) => setReviewRequestForm({...reviewRequestForm, request_type: e.target.value})}
            >
              <option value="">Select Review Type</option>
              <option value="tenant_review">Tenant Review</option>
              <option value="landlord_review">Landlord Review</option>
            </select>
            <input
              type="text"
              placeholder="Reviewer User ID or Email"
              value={reviewRequestForm.reviewer_id || reviewRequestForm.reviewer_email}
              onChange={(e) => {
                if (e.target.value.includes('@')) {
                  setReviewRequestForm({...reviewRequestForm, reviewer_email: e.target.value, reviewer_id: ''});
                } else {
                  setReviewRequestForm({...reviewRequestForm, reviewer_id: e.target.value, reviewer_email: ''});
                }
              }}
            />
            <input
              type="text"
              placeholder="Property ID or Address"
              value={reviewRequestForm.property_id}
              onChange={(e) => setReviewRequestForm({...reviewRequestForm, property_id: e.target.value})}
            />
            <textarea
              placeholder="Message to reviewer"
              value={reviewRequestForm.message}
              onChange={(e) => setReviewRequestForm({...reviewRequestForm, message: e.target.value})}
              rows="3"
            />
            <button onClick={handleReviewRequest}>Send Review Request</button>
          </div>
        </div>

        {/* Review Response Section */}
        <div className="review-section">
          <h3>📊 Submit Review</h3>
          <div className="form">
            <select 
              value={reviewResponseForm.request_id} 
              onChange={(e) => setReviewResponseForm({...reviewResponseForm, request_id: e.target.value})}
            >
              <option value="">Select Request to Review</option>
              {filteredData.review_requests.filter(req => req.status === 'pending').map(req => (
                <option key={req.id} value={req.id}>
                  {req.request_type} - {req.requester_id}
                </option>
              ))}
            </select>
            
            <div className="rating-grid">
              {['payment_reliability', 'property_maintenance', 'communication', 'lease_compliance', 
                'responsiveness', 'property_condition', 'fairness', 'privacy_respect'].map(category => (
                <div key={category} className="rating-item">
                  <label>{category.replace('_', ' ').toUpperCase()}:</label>
                  <select 
                    value={reviewResponseForm[category] || ''} 
                    onChange={(e) => setReviewResponseForm({...reviewResponseForm, [category]: parseInt(e.target.value)})}
                  >
                    <option value="">Rate 1-5</option>
                    <option value="1">1 - Poor</option>
                    <option value="2">2 - Fair</option>
                    <option value="3">3 - Good</option>
                    <option value="4">4 - Very Good</option>
                    <option value="5">5 - Excellent</option>
                  </select>
                </div>
              ))}
            </div>
            
            <select 
              value={reviewResponseForm.overall_rating} 
              onChange={(e) => setReviewResponseForm({...reviewResponseForm, overall_rating: parseInt(e.target.value)})}
            >
              <option value="">Overall Rating (1-5)</option>
              <option value="1">1 - Poor</option>
              <option value="2">2 - Fair</option>
              <option value="3">3 - Good</option>
              <option value="4">4 - Very Good</option>
              <option value="5">5 - Excellent</option>
            </select>
            
            <textarea
              placeholder="Detailed comments about your experience"
              value={reviewResponseForm.comments}
              onChange={(e) => setReviewResponseForm({...reviewResponseForm, comments: e.target.value})}
              rows="4"
            />
            
            <button onClick={handleReviewResponse}>Submit Review for AI Analysis</button>
          </div>
        </div>

        {/* Review Results */}
        <div className="review-results">
          <h3>🤖 AI Analysis Results ({filteredData.review_responses.length})</h3>
          {filteredData.review_responses.map(response => (
            <div key={response.id} className="review-result-item">
              <div className="ai-score-header">
                <h4>AI Score: {response.ai_overall_score}/10</h4>
                <span className={`risk-badge risk-${response.ai_risk_assessment}`}>
                  {response.ai_risk_assessment.toUpperCase()} RISK
                </span>
              </div>
              
              <div className="flags-section">
                {response.ai_green_flags && response.ai_green_flags.length > 0 && (
                  <div className="green-flags">
                    <strong>🟢 Green Flags:</strong>
                    <ul>
                      {response.ai_green_flags.map((flag, idx) => (
                        <li key={idx}>{flag}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                {response.ai_red_flags && response.ai_red_flags.length > 0 && (
                  <div className="red-flags">
                    <strong>🔴 Red Flags:</strong>
                    <ul>
                      {response.ai_red_flags.map((flag, idx) => (
                        <li key={idx}>{flag}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              
              <div className="ai-summary">
                <strong>📝 AI Analysis:</strong>
                <p>{response.ai_analysis_summary}</p>
              </div>
              
              <div className="review-meta">
                <small>Submitted: {new Date(response.created_at).toLocaleString()}</small>
              </div>
            </div>
          ))}
          {filteredData.review_responses.length === 0 && (
            <p>No AI reviews yet. Submit your first review above!</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIReviews; 