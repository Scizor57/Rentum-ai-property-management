import React from 'react';

const Dashboard = ({ currentUser, users, properties, filteredData, ocrScans, setActiveTab }) => {
  // Get property information from OCR scans
  const getPropertyFromOCR = () => {
    if (!ocrScans || ocrScans.length === 0) return null;
    
    const propertyScans = ocrScans.filter(scan => 
      scan.extracted_data && (
        scan.extracted_data.property_address ||
        scan.extracted_data.rent_amount ||
        scan.document_type === 'lease_agreement' ||
        scan.document_type === 'rental_agreement'
      )
    );
    
    return propertyScans.length > 0 ? propertyScans[0] : null;
  };

  const propertyData = getPropertyFromOCR();

  return (
    <div className="section">
      <h2>🏠 Welcome, {currentUser.name}!</h2>
      <div className="user-info">
        <p><strong>Role:</strong> {currentUser.role.toUpperCase()}</p>
        <p><strong>Email:</strong> {currentUser.email}</p>
        <p><strong>Member since:</strong> {new Date(currentUser.created_at).toLocaleDateString()}</p>
      </div>
      
      {/* Property Details Quick Access */}
      {propertyData && (
        <div className="dashboard-property-card">
          <h3>🏠 Your Property Details</h3>
          <div className="property-quick-info">
            <div className="property-row">
              <span><strong>Address:</strong> {propertyData.extracted_data.property_address || 'N/A'}</span>
              <span><strong>Monthly Rent:</strong> ${propertyData.extracted_data.rent_amount || 'N/A'}</span>
            </div>
            {propertyData.extracted_data.property_type && (
              <div className="property-row">
                <span><strong>Type:</strong> {propertyData.extracted_data.property_type}</span>
                <span><strong>Confidence:</strong> 
                  <span className={`confidence ${propertyData.confidence_score >= 0.8 ? 'high' : propertyData.confidence_score >= 0.6 ? 'medium' : 'low'}`}>
                    {(propertyData.confidence_score * 100).toFixed(1)}%
                  </span>
                </span>
              </div>
            )}
            <div className="property-actions">
              <button 
                onClick={() => setActiveTab('property-details')}
                className="view-details-btn"
              >
                📋 View Full Property Details
              </button>
            </div>
          </div>
        </div>
      )}

      {/* If no property data from OCR */}
      {!propertyData && (
        <div className="dashboard-property-card no-property">
          <h3>🏠 Property Information</h3>
          <p>No property details found. Upload a lease agreement or rental document in the OCR Scanner to see your property information here.</p>
          <div className="property-actions">
            <button 
              onClick={() => setActiveTab('ocr-scanner')}
              className="scan-document-btn"
            >
              📄 Scan Property Document
            </button>
          </div>
        </div>
      )}
      
      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>OCR Scans</h3>
          <div className="stat-number">{ocrScans ? ocrScans.length : 0}</div>
        </div>
        <div className="stat-card">
          <h3>Documents</h3>
          <div className="stat-number">{filteredData.documents.length}</div>
        </div>
        <div className="stat-card">
          <h3>Messages</h3>
          <div className="stat-number">{filteredData.chat.length}</div>
        </div>
        <div className="stat-card">
          <h3>Issues</h3>
          <div className="stat-number">{filteredData.issues.length}</div>
        </div>
      </div>

      <div className="recent-activity">
        <h3>Recent Activity</h3>
        <ul>
          {filteredData.notifications.slice(0, 5).map(n => (
            <li key={n.id}>
              <strong>{n.notif_type.replace('_', ' ').toUpperCase()}</strong> - {n.content}
            </li>
          ))}
          {filteredData.notifications.length === 0 && <li>No recent notifications</li>}
        </ul>
      </div>

      <style jsx>{`
        .dashboard-property-card {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 2rem;
          border-radius: 12px;
          margin: 2rem 0;
          box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }

        .dashboard-property-card.no-property {
          background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
          text-align: center;
        }

        .dashboard-property-card h3 {
          margin: 0 0 1.5rem 0;
          font-size: 1.5rem;
        }

        .property-quick-info {
          background: rgba(255,255,255,0.1);
          padding: 1.5rem;
          border-radius: 8px;
          backdrop-filter: blur(10px);
        }

        .property-row {
          display: flex;
          justify-content: space-between;
          margin: 1rem 0;
          flex-wrap: wrap;
          gap: 1rem;
        }

        .property-row span {
          font-size: 0.95rem;
        }

        .confidence.high {
          color: #00ff88;
          font-weight: bold;
        }

        .confidence.medium {
          color: #ffeb3b;
          font-weight: bold;
        }

        .confidence.low {
          color: #ff6b6b;
          font-weight: bold;
        }

        .property-actions {
          text-align: center;
          margin-top: 1.5rem;
        }

        .view-details-btn, .scan-document-btn {
          background: rgba(255,255,255,0.2);
          color: white;
          border: 2px solid rgba(255,255,255,0.3);
          padding: 0.8rem 2rem;
          border-radius: 25px;
          cursor: pointer;
          font-weight: bold;
          transition: all 0.3s ease;
          backdrop-filter: blur(10px);
        }

        .view-details-btn:hover, .scan-document-btn:hover {
          background: rgba(255,255,255,0.3);
          border-color: rgba(255,255,255,0.5);
          transform: translateY(-2px);
          box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .dashboard-stats {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1.5rem;
          margin: 2rem 0;
        }

        .stat-card {
          background: white;
          padding: 1.5rem;
          border-radius: 8px;
          text-align: center;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          border: 1px solid #e0e0e0;
        }

        .stat-card h3 {
          margin: 0 0 1rem 0;
          color: #333;
          font-size: 1rem;
        }

        .stat-number {
          font-size: 2.5rem;
          font-weight: bold;
          color: #667eea;
        }
      `}</style>
    </div>
  );
};

export default Dashboard; 