import React, { useState } from 'react';

const Settings = () => {
  const [formData, setFormData] = useState({
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password === '' || formData.confirmPassword === '') {
      setError('Please fill in all fields');
    } else if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
    } else {
      try {
        const response = await changePassword(formData.password);
        if (response.ok) {
          console.log('Password changed successfully');
          setFormData({ password: '', confirmPassword: '' });
          setError('');
        } else {
          setError('Failed to change password. Please try again.');
          console.error('Password change error:', response.statusText);
        }
      } catch (error) {
        setError('Failed to change password. Please try again.');
        console.error('Password change error:', error);
      }
    }
  };

  const changePassword = async (newPassword) => {
    try {
      const response = await fetch('your-backend-change-password-endpoint', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ newPassword })
      });
      return response;
    } catch (error) {
      throw new Error('Error changing password:', error);
    }
  };

  return (
    <div>
      <h2>Settings</h2>
      {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          name="password"
          placeholder="New Password"
          value={formData.password}
          onChange={handleChange}
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm New Password"
          value={formData.confirmPassword}
          onChange={handleChange}
        />
        <button type="submit">Save Changes</button>
      </form>
    </div>
  );
}

export default Settings;
