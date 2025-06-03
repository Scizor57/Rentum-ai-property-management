import React from 'react';

const Login = ({ 
  darkMode, 
  setDarkMode, 
  users, 
  loginForm, 
  handleLoginChange, 
  handleLogin, 
  userForm, 
  handleUserChange, 
  addUser, 
  isRegistering,
  urlParams,
  setLoginForm,
  apiConnected
}) => {
  return (
    <div className={`App ${darkMode ? 'dark-mode' : ''}`}>
      <div className="header">
        <h1>🏠 Rentum AI - Property Management Platform</h1>
        <button 
          className="theme-toggle"
          onClick={() => setDarkMode(!darkMode)}
          title={`Switch to ${darkMode ? 'light' : 'dark'} mode`}
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </div>
      
      <div className="login-container">
        <div className="login-section">
          <h2>🔐 Login to Your Account</h2>
          <form onSubmit={handleLogin} className="form">
            <input 
              name="email" 
              placeholder="Email Address" 
              value={loginForm.email} 
              onChange={handleLoginChange} 
              required 
            />
            <select name="role" value={loginForm.role} onChange={handleLoginChange}>
              <option value="tenant">Tenant</option>
              <option value="landlord">Landlord</option>
              <option value="company">Company</option>
            </select>
            <button type="submit">Login</button>
          </form>
          
          <div className="demo-accounts">
            <h3>Demo Accounts {users.length > 0 ? `(${users.length} found)` : '(Loading...)'}</h3>
            {users.length === 0 && (
              <div className="loading-message">
                <p>🔄 Loading demo accounts from backend...</p>
                <p><small>If this takes too long, there might be an API connection issue.</small></p>
              </div>
            )}
            <div className="demo-list">
              {users.map(user => (
                <div key={user.id} className="demo-account">
                  <strong>{user.name}</strong> ({user.role})
                  <br />Email: {user.email}
                  <button 
                    onClick={() => setLoginForm({ email: user.email, role: user.role })}
                    className="quick-login"
                  >
                    Quick Login
                  </button>
                </div>
              ))}
              {users.length === 0 && (
                <div className="fallback-demo">
                  <p>🚀 <strong>Quick Demo Access:</strong></p>
                  <div className="demo-account">
                    <strong>Demo Tenant</strong> (tenant)
                    <br />Email: tenant@demo.com
                    <button 
                      onClick={() => setLoginForm({ email: 'tenant@demo.com', role: 'tenant' })}
                      className="quick-login"
                    >
                      Quick Login
                    </button>
                  </div>
                  <div className="demo-account">
                    <strong>Demo Landlord</strong> (landlord)
                    <br />Email: landlord@demo.com
                    <button 
                      onClick={() => setLoginForm({ email: 'landlord@demo.com', role: 'landlord' })}
                      className="quick-login"
                    >
                      Quick Login
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
        
        <div className="register-section">
          <h2>📝 Register New Account</h2>
          <form onSubmit={addUser} className="form">
            <input name="name" placeholder="Full Name" value={userForm.name} onChange={handleUserChange} required />
            <input name="email" placeholder="Email Address" value={userForm.email} onChange={handleUserChange} required />
            <input name="phone" placeholder="Phone Number" value={userForm.phone} onChange={handleUserChange} />
            {urlParams && (
              <div className="url-join-notice">
                <p>🔗 You're joining as a <strong>{urlParams.role}</strong> through an invitation link</p>
              </div>
            )}
            <select name="role" value={userForm.role} onChange={handleUserChange} disabled={urlParams !== null}>
              <option value="tenant">Tenant</option>
              <option value="landlord">Landlord</option>
              <option value="company">Company</option>
            </select>
            <button type="submit" disabled={isRegistering}>
              {isRegistering ? '⏳ Registering...' : 'Register'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login; 