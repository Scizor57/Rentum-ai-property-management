import React from 'react';

function PropertyDetails({ ocrScans, currentUser, darkMode }) {
  // Get the most recent OCR scan that contains property information
  const getPropertyFromOCR = () => {
    if (!ocrScans || ocrScans.length === 0) return null;
    
    // Find OCR scans that contain property-related information
    const propertyScans = ocrScans.filter(scan => 
      scan.extracted_data && (
        scan.extracted_data.property_address ||
        scan.extracted_data.rent_amount ||
        scan.extracted_data.property_type ||
        scan.document_type === 'lease_agreement' ||
        scan.document_type === 'rental_agreement'
      )
    );
    
    // Return the most recent property scan
    return propertyScans.length > 0 ? propertyScans[0] : null;
  };

  const propertyData = getPropertyFromOCR();

  if (!currentUser) {
    return (
      <div className={`section ${darkMode ? 'dark' : 'light'}`}>
        <h2>🏠 Property Details</h2>
        <p>Please log in to view property details.</p>
      </div>
    );
  }

  if (!propertyData) {
    return (
      <div className={`section ${darkMode ? 'dark' : 'light'}`}>
        <h2>🏠 Property Details</h2>
        <div className="no-data">
          <p>📄 No property information available yet.</p>
          <p>Upload a lease agreement or rental document in the OCR Scanner to see property details here.</p>
        </div>
      </div>
    );
  }

  const extractedData = propertyData.extracted_data;
  const confidenceScore = propertyData.confidence_score;

  return (
    <div className={`section ${darkMode ? 'dark' : 'light'}`}>
      <h2>🏠 Property Details</h2>
      
      <div className="property-overview">
        <div className="scan-info">
          <p><strong>📄 Source Document:</strong> {propertyData.document_type?.replace('_', ' ').toUpperCase()}</p>
          <p><strong>📅 Scanned:</strong> {new Date(propertyData.created_at).toLocaleString()}</p>
          <p><strong>🎯 Confidence:</strong> 
            <span className={`confidence ${confidenceScore >= 0.8 ? 'high' : confidenceScore >= 0.6 ? 'medium' : 'low'}`}>
              {(confidenceScore * 100).toFixed(1)}%
            </span>
          </p>
        </div>
      </div>

      <div className="property-grid">
        {/* Property Address */}
        {extractedData.property_address && (
          <div className="property-card">
            <h3>📍 Property Address</h3>
            <p className="property-value">{extractedData.property_address}</p>
          </div>
        )}

        {/* Property Type */}
        {extractedData.property_type && (
          <div className="property-card">
            <h3>🏡 Property Type</h3>
            <p className="property-value">{extractedData.property_type}</p>
          </div>
        )}

        {/* Rent Information */}
        {extractedData.rent_amount && (
          <div className="property-card">
            <h3>💰 Monthly Rent</h3>
            <p className="property-value">${extractedData.rent_amount}</p>
          </div>
        )}

        {/* Lease Duration */}
        {(extractedData.lease_start_date || extractedData.lease_end_date) && (
          <div className="property-card">
            <h3>📅 Lease Period</h3>
            <div className="lease-dates">
              {extractedData.lease_start_date && (
                <p><strong>Start:</strong> {extractedData.lease_start_date}</p>
              )}
              {extractedData.lease_end_date && (
                <p><strong>End:</strong> {extractedData.lease_end_date}</p>
              )}
            </div>
          </div>
        )}

        {/* Security Deposit */}
        {extractedData.security_deposit && (
          <div className="property-card">
            <h3>🔒 Security Deposit</h3>
            <p className="property-value">${extractedData.security_deposit}</p>
          </div>
        )}

        {/* Landlord Information */}
        {extractedData.landlord_name && (
          <div className="property-card">
            <h3>👤 Landlord</h3>
            <p className="property-value">{extractedData.landlord_name}</p>
            {extractedData.landlord_contact && (
              <p className="contact-info">{extractedData.landlord_contact}</p>
            )}
          </div>
        )}

        {/* Tenant Information */}
        {extractedData.tenant_name && (
          <div className="property-card">
            <h3>🏠 Tenant</h3>
            <p className="property-value">{extractedData.tenant_name}</p>
          </div>
        )}

        {/* Additional Terms */}
        {extractedData.key_terms && extractedData.key_terms.length > 0 && (
          <div className="property-card full-width">
            <h3>📋 Key Terms & Conditions</h3>
            <ul className="terms-list">
              {extractedData.key_terms.map((term, index) => (
                <li key={index}>{term}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Utilities Information */}
        {extractedData.utilities_included && (
          <div className="property-card">
            <h3>⚡ Utilities</h3>
            <p className="property-value">{extractedData.utilities_included}</p>
          </div>
        )}

        {/* Pet Policy */}
        {extractedData.pet_policy && (
          <div className="property-card">
            <h3>🐕 Pet Policy</h3>
            <p className="property-value">{extractedData.pet_policy}</p>
          </div>
        )}
      </div>

      {/* Raw Data Section for Debugging */}
      {confidenceScore < 0.7 && (
        <div className="raw-data-section">
          <h3>⚠️ Low Confidence Data</h3>
          <p>Some information may need verification. Please review the scanned document for accuracy.</p>
        </div>
      )}

      <style jsx>{`
        .property-overview {
          background: ${darkMode ? '#2a2a2a' : '#f8f9fa'};
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 2rem;
        }

        .scan-info {
          display: flex;
          gap: 2rem;
          flex-wrap: wrap;
        }

        .scan-info p {
          margin: 0.5rem 0;
          font-size: 0.9rem;
        }

        .confidence.high {
          color: #28a745;
          font-weight: bold;
        }

        .confidence.medium {
          color: #ffc107;
          font-weight: bold;
        }

        .confidence.low {
          color: #dc3545;
          font-weight: bold;
        }

        .property-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }

        .property-card {
          background: ${darkMode ? '#1e1e1e' : '#ffffff'};
          border: 1px solid ${darkMode ? '#444' : '#ddd'};
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .property-card.full-width {
          grid-column: 1 / -1;
        }

        .property-card h3 {
          margin: 0 0 1rem 0;
          color: ${darkMode ? '#fff' : '#333'};
          font-size: 1.1rem;
        }

        .property-value {
          font-size: 1.2rem;
          font-weight: bold;
          color: ${darkMode ? '#4fc3f7' : '#007bff'};
          margin: 0;
        }

        .lease-dates p {
          margin: 0.5rem 0;
        }

        .contact-info {
          font-size: 0.9rem;
          color: ${darkMode ? '#bbb' : '#666'};
          margin: 0.5rem 0 0 0;
        }

        .terms-list {
          list-style-type: disc;
          padding-left: 1.5rem;
          margin: 0;
        }

        .terms-list li {
          margin: 0.5rem 0;
          color: ${darkMode ? '#ddd' : '#555'};
        }

        .no-data {
          text-align: center;
          padding: 3rem;
          color: ${darkMode ? '#bbb' : '#666'};
        }

        .raw-data-section {
          background: #fff3cd;
          border: 1px solid #ffeaa7;
          border-radius: 8px;
          padding: 1rem;
          margin-top: 2rem;
        }

        .raw-data-section h3 {
          color: #856404;
          margin: 0 0 0.5rem 0;
        }

        .raw-data-section p {
          color: #856404;
          margin: 0;
        }
      `}</style>
    </div>
  );
}

export default PropertyDetails; 