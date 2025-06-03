import React from 'react';

const Payments = ({ 
  currentUser,
  filteredData, 
  paymentForm, 
  handlePaymentChange, 
  addPayment,
  setPaymentForm 
}) => {
  return (
    <div className="section">
      <h2>💳 {currentUser.role === 'landlord' ? 'Payment Collection' : 'Payment Management'}</h2>
      <form onSubmit={addPayment} className="form">
        <input 
          name="property_id" 
          type="text" 
          placeholder="Property ID or Description" 
          value={paymentForm.property_id} 
          onChange={handlePaymentChange} 
          required 
        />
        <input name="amount" type="number" placeholder="Amount (INR)" value={paymentForm.amount} onChange={handlePaymentChange} required />
        <select name="payment_type" value={paymentForm.payment_type} onChange={handlePaymentChange} required>
          <option value="">Select Payment Type</option>
          <option value="rent">Monthly Rent</option>
          <option value="deposit">Security Deposit</option>
          <option value="wallet_topup">Wallet Top-up</option>
          <option value="maintenance">Maintenance</option>
          <option value="other">Other</option>
        </select>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setPaymentForm({...paymentForm, proof_file: e.target.files[0]})}
        />
        <button type="submit">{currentUser.role === 'landlord' ? 'Record Payment Received' : 'Record Payment Made'}</button>
      </form>
      <div className="list-container">
        <h3>Payments ({filteredData.payments.length})</h3>
        <ul>
          {filteredData.payments.map(p => (
            <li key={p.id}>
              <strong>INR {p.amount}</strong> - {p.payment_type.replace('_', ' ')}
              <span className={`status-${p.status}`}> • {p.status}</span>
              {p.proof_file && <><br />Proof: <a href={p.proof_url} target="_blank" rel="noopener noreferrer">View Proof</a></>}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Payments; 