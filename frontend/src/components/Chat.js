import React from 'react';

const Chat = ({ 
  currentUser, 
  filteredData, 
  chatForm, 
  handleChatChange, 
  addChat 
}) => {
  return (
    <div className="section">
      <h2>💬 Messages</h2>
      <form onSubmit={addChat} className="form">
        <input name="to_user_id" placeholder="To User ID" value={chatForm.to_user_id} onChange={handleChatChange} required />
        <input 
          name="property_id" 
          placeholder="Property ID (optional)" 
          value={chatForm.property_id} 
          onChange={handleChatChange} 
        />
        <textarea name="message" placeholder="Type your message..." value={chatForm.message} onChange={handleChatChange} required rows="3"></textarea>
        <button type="submit">Send Message</button>
      </form>
      <div className="list-container">
        <h3>My Messages ({filteredData.chat.length})</h3>
        <ul>
          {filteredData.chat.map(c => (
            <li key={c.id}>
              <strong>{c.from_user_id === currentUser.id ? 'You' : c.from_user_id} to {c.to_user_id === currentUser.id ? 'You' : c.to_user_id}</strong>
              {c.property_id && <span> | Property: {c.property_id}</span>}
              <br />"{c.message}"
              <br /><small>{new Date(c.created_at).toLocaleString()}</small>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Chat; 