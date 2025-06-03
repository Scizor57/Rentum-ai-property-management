import React from 'react';

const Issues = ({ 
  currentUser, 
  filteredData, 
  issueForm, 
  handleIssueChange, 
  addIssue 
}) => {
  return (
    <div className="section">
      <h2>🔧 {currentUser.role === 'landlord' ? 'Property Issues Management' : 'Report Issues'}</h2>
      {currentUser.role === 'tenant' && (
        <form onSubmit={addIssue} className="form">
          <input 
            name="property_id" 
            type="text" 
            placeholder="Property ID or Address" 
            value={issueForm.property_id} 
            onChange={handleIssueChange} 
            required 
          />
          <textarea name="details" placeholder="Describe the issue..." value={issueForm.details} onChange={handleIssueChange} required rows="3"></textarea>
          <button type="submit">Report Issue</button>
        </form>
      )}
      <div className="list-container">
        <h3>{currentUser.role === 'landlord' ? 'Property Issues' : 'My Reported Issues'} ({filteredData.issues.length})</h3>
        <ul>
          {filteredData.issues.map(i => (
            <li key={i.id}>
              <strong>Property {i.property_id}</strong>
              <span className={`status-${i.status}`}> • {i.status}</span>
              {currentUser.role === 'landlord' && <><br />Reported by: {i.raised_by}</>}
              <br />"{i.details}"
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Issues; 