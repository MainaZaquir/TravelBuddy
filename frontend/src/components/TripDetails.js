import React, { useState } from 'react';

const TripDetails = ({ trip }) => {
  const [requestSent, setRequestSent] = useState(false);
  const [error, setError] = useState('');

  const handleJoinTrip = async () => {
    try {
      const response = await fetch(`your-backend-join-trip-endpoint/${trip.id}`, {
        method: 'POST',
      });
      if (response.ok) {
        setRequestSent(true);
           console.log('Successfully joined the trip');
      } else {
        setError('Failed to join the trip');
        console.error('Failed to join the trip:', response.statusText);
      }
    } catch (error) {
      setError('Failed to join the trip');
      console.error('Failed to join the trip:', error);
    }
  };

  return (
    <div>
      <h2>Trip Details</h2>
      <div>
        <h3>{trip.destination}</h3>
        <p>Dates: {trip.dates}</p>
        <p>Description: {trip.description}</p>
        <p>Duration: {trip.duration}</p>
        <p>Price: {trip.price}</p>
        <p>Available Seats: {trip.availableSeats}</p>
      </div>
      <button onClick={handleJoinTrip} disabled={requestSent}>
        {requestSent ? 'Request Sent' : 'Join Trip'}
      </button>
      {error && <p>{error}</p>}
    </div>
  );
}

export default TripDetails;