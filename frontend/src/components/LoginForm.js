import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const LoginForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loggedIn, setLoggedIn] = useState(false); // This state is going to track a successful login

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.username === '' || formData.password === '') {
      setError('Please fill in all fields');
    } else {
      try {
        const response = await fetch('your-backend-login-endpoint', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        });
        if (response.ok) {
          // Handles a successful login
          console.log('Login successful');
          setLoggedIn(true); // Set loggedIn state to true
        } else {
          // Handles a login error
          setError('Login failed. Please try again.');
        }
      } catch (error) {
        // Handles a login error
        setError('Login failed. Please try again.');
        console.error('Login error:', error);
      }
    }
  };

  // Redirects to the Dashboard component if logged in
  //if (loggedIn) {
   // return <Redirect to="/dashboard" />;
  //}

  return (
    <div className="login-container">
      <h2>Login</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          className="login-input"
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          className="login-input"
        />
        <button type="submit" className="login-button">Login</button>
      </form>
      <p className="signup-link">Don't have an account? <Link to="/signup">Sign up here</Link></p>
    </div>
  );
}

export default LoginForm;
