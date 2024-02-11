import React, { useState, useEffect } from 'react';
import './Profile.css'; 

const Profile = () => {
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    interests: ''
  });
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch('your-backend-profile-endpoint');
      const data = await response.json();
      if (response.ok) {
        setFormData({
          username: data.username,
          email: data.email,
          interests: data.interests
        });
      } else {
        setError('Error fetching user profile');
      }
    } catch (error) {
      setError('Error fetching user profile');
      console.error('Error fetching user profile:', error);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Validation and submission logic
  };

  return (
    <div className="profile-container">
      <h2>Profile</h2>
      {error && <p>{error}</p>}
      {editing ? (
        <form onSubmit={handleSubmit} className="profile-form">
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
          />
          <input
            type="text"
            name="interests"
            placeholder="Interests"
            value={formData.interests}
            onChange={handleChange}
          />
          <button type="submit">Save Changes</button>
        </form>
      ) : (
        <div className="profile-details">
          <p>Username: {formData.username}</p>
          <p>Email: {formData.email}</p>
          <p>Interests: {formData.interests}</p>
          <button className="edit-profile-button" onClick={() => setEditing(true)}>Edit Profile</button>
        </div>
      )}
    </div>
  );
}

export default Profile;
