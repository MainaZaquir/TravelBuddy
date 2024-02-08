import React, { useState, useEffect } from 'react';

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
    if (formData.username === '' || formData.email === '' || formData.interests === '') {
      setError('Please fill in all fields');
    } else {
      try {
        const response = await fetch('your-backend-edit-profile-endpoint', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        });
        // Handles a successful profile update
        if (response.ok) {
          console.log('Profile updated successfully:', response);
          setEditing(false);
        } else {
          setError('Failed to update profile. Please try again.');
        }
      } catch (error) {
        // Handles a profile update error
        setError('Failed to update profile. Please try again.');
        console.error('Profile update error:', error);
      }
    }
  };

  return (
    <div>
      <h2>Profile</h2>
      {error && <p>{error}</p>}
      {editing ? (
        <form onSubmit={handleSubmit}>
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
        <div>
          {/* Displays the user profile details */}
          <div>
            <p>Username: {formData.username}</p>
            <p>Email: {formData.email}</p>
            <p>Interests: {formData.interests}</p>
          </div>
          <button onClick={() => setEditing(true)}>Edit Profile</button>
        </div>
      )}
    </div>
  );
}

export default Profile;
