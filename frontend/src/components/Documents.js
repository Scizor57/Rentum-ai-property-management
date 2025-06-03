import React from 'react';

const Documents = ({ 
  filteredData, 
  documentForm, 
  handleDocumentChange, 
  addDocument,
  setDocumentForm 
}) => {
  return (
    <div className="section">
      <h2>📄 Document Vault</h2>
      <form onSubmit={addDocument} className="form">
        <input 
          name="property_id" 
          type="text" 
          placeholder="Property ID (optional)" 
          value={documentForm.property_id} 
          onChange={handleDocumentChange} 
        />
        <select name="doc_type" value={documentForm.doc_type} onChange={handleDocumentChange} required>
          <option value="">Select Document Type</option>
          <option value="aadhaar">Aadhaar Card</option>
          <option value="pan">PAN Card</option>
          <option value="police_verification">Police Verification</option>
          <option value="rental_agreement">Rental Agreement</option>
          <option value="payment_proof">Payment Proof</option>
          <option value="other">Other</option>
        </select>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setDocumentForm({...documentForm, file: e.target.files[0]})}
        />
        <button type="submit">Upload Document</button>
      </form>
      <div className="list-container">
        <h3>My Documents ({filteredData.documents.length})</h3>
        <ul>
          {filteredData.documents.map(d => (
            <li key={d.id}>
              <strong>{d.doc_type.replace('_', ' ').toUpperCase()}</strong>
              {d.property_id && <><br />Property: {d.property_id}</>}
              <br />Link: <a href={d.url} target="_blank" rel="noopener noreferrer">View Document</a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Documents; 