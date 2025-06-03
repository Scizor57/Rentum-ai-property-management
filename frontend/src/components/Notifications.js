import React from 'react';

const Notifications = ({ filteredData }) => {
  return (
    <div className="section">
      <h2>🔔 Notifications</h2>
      <div className="list-container">
        <h3>My Notifications ({filteredData.notifications.length})</h3>
        <ul>
          {filteredData.notifications.map(n => (
            <li key={n.id}>
              <strong>{n.notif_type.replace('_', ' ').toUpperCase()}</strong> via {n.method}
              <span className={`status-${n.status}`}> • {n.status}</span>
              <br />"{n.content}"
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Notifications; 