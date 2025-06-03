import React from 'react';

const Profile = ({ currentUser, userProfile, setUserProfile, API_BASE }) => {
  return (
    <div className="section">
      <h2>👤 AI-Powered Profile</h2>
      <div className="profile-container">
        {userProfile ? (
          <div className="profile-card">
            <div className="profile-header">
              <h3>{currentUser.name}</h3>
              <div className="ai-score-display">
                <span className="score-number">{userProfile.overall_ai_score || 0}</span>
                <span className="score-label">AI Score</span>
              </div>
            </div>
            
            <div className="profile-stats">
              <div className="stat-item">
                <strong>Total Reviews:</strong> {userProfile.total_reviews}
              </div>
              
              <div className="category-scores">
                <h4>📊 Category Breakdown:</h4>
                {['payment_reliability', 'property_maintenance', 'communication', 'lease_compliance'].map(category => (
                  <div key={category} className="category-item">
                    <span>{category.replace('_', ' ').toUpperCase()}:</span>
                    <div className="score-bar">
                      <div 
                        className="score-fill" 
                        style={{width: `${(userProfile[`avg_${category}`] || 0) * 20}%`}}
                      ></div>
                      <span>{(userProfile[`avg_${category}`] || 0).toFixed(1)}/5</span>
                    </div>
                  </div>
                ))}
              </div>
              
              {userProfile.green_flags_count && Object.keys(userProfile.green_flags_count).length > 0 && (
                <div className="flags-summary">
                  <h4>🟢 Positive Traits:</h4>
                  {Object.entries(userProfile.green_flags_count).map(([flag, count]) => (
                    <span key={flag} className="flag-badge green">
                      {flag} ({count})
                    </span>
                  ))}
                </div>
              )}
              
              {userProfile.red_flags_count && Object.keys(userProfile.red_flags_count).length > 0 && (
                <div className="flags-summary">
                  <h4>🔴 Areas for Improvement:</h4>
                  {Object.entries(userProfile.red_flags_count).map(([flag, count]) => (
                    <span key={flag} className="flag-badge red">
                      {flag} ({count})
                    </span>
                  ))}
                </div>
              )}
            </div>
            
            <div className="profile-footer">
              <small>Last Updated: {new Date(userProfile.last_updated).toLocaleString()}</small>
            </div>
          </div>
        ) : (
          <div className="profile-loading">
            <p>Loading AI profile data...</p>
            <button onClick={() => {
              fetch(`${API_BASE}/users/${currentUser.id}/profile`)
                .then(res => res.json())
                .then(setUserProfile);
            }}>
              Refresh Profile
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile; 