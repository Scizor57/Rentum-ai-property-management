import React from 'react';

const OCRScanner = ({ 
  currentUser, 
  filteredData, 
  ocrForm, 
  setOcrForm, 
  handleOcrUpload 
}) => {
  return (
    <div className="section">
      <h2>🔍 AI Document Scanner</h2>
      <div className="ocr-container">
        <div className="upload-section">
          <h3>📄 Upload Any Document for AI Analysis</h3>
          <div className="form">
            <select 
              value={ocrForm.document_type} 
              onChange={(e) => setOcrForm({...ocrForm, document_type: e.target.value})}
            >
              <option value="">Select Document Type</option>
              <option value="rental_agreement">Rental Agreement</option>
              <option value="id_card">ID Card (Aadhaar/PAN/Driving License)</option>
              <option value="property_document">Property Document</option>
            </select>
            <input
              type="file"
              accept="image/*,application/pdf"
              onChange={(e) => setOcrForm({...ocrForm, file: e.target.files[0]})}
            />
            <button onClick={handleOcrUpload} disabled={!ocrForm.file || !ocrForm.document_type}>
              🚀 Scan Document with AI
            </button>
            <p className="upload-note">
              📝 Supported formats: Images (JPG, PNG) and PDF files
              <br />🤖 AI will extract key information and auto-fill relevant forms
              <br />📋 Supported: Rental Agreements, ID Cards, Property Documents
            </p>
          </div>
        </div>
        
        <div className="ocr-results">
          <h3>📊 AI Scan Results ({filteredData.ocr_scans.length})</h3>
          {filteredData.ocr_scans.map(scan => (
            <div key={scan.id} className="ocr-result-item">
              <div className="scan-header">
                <strong>📄 {scan.document_type.replace('_', ' ').toUpperCase()}</strong>
                <span className={`status status-${scan.status}`}>{scan.status}</span>
              </div>
              
              <div className="extracted-data">
                <h4>🤖 AI Extracted Information:</h4>
                {Object.entries(scan.extracted_data).map(([key, value]) => (
                  <div key={key} className="data-field">
                    <strong>{key.replace('_', ' ').toUpperCase()}:</strong> {value}
                    <span className="confidence">
                      ({scan.confidence_scores[key] || 0}% confidence)
                    </span>
                  </div>
                ))}
              </div>
              
              <div className="scan-meta">
                <small>Scanned: {new Date(scan.created_at).toLocaleString()}</small>
                <br />
                <small>✨ Information auto-filled in relevant forms</small>
              </div>
            </div>
          ))}
          {filteredData.ocr_scans.length === 0 && (
            <p>No documents scanned yet. Upload your first document above!</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default OCRScanner; 