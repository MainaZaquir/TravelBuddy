import React, { useState, useEffect } from 'react';
import './Profile.css'; 
import { useParams} from "react-router-dom";


const Profile = () => {
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    interests: ''
  });
  const [error, setError] = useState('');
  
  const {id} = useParams();

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const response = await fetch(`/profile/${id}`);
        if (response.ok) {
          const data = await response.json();
          setFormData({
            username: data.username,
            email: data.email,
            interests: data.interests
          });
        } else {
          const errorMessage = await response.text();
          setError(`Error fetching user profile: ${errorMessage}`);
        }
      } catch (error) {
        setError('Error fetching user profile');
        console.error('Error fetching user profile:', error);
      }
    };
  
    fetchUserProfile(); // Call the function immediately
  
  }, [id]); // Empty dependency array since we want it to run only once

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:5555/profile/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      if (response.ok) {
        console.log('Profile updated successfully');
        setEditing(false); 
      } else {
        const errorMessage = await response.text();
        setError(`Failed to update profile: ${errorMessage}`);
        console.error('Profile update error:', errorMessage);
      }
    } catch (error) {
      setError('Failed to update profile. Please try again.');
      console.error('Profile update error:', error);
    }
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
