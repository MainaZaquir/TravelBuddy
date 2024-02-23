import React, { useState, useEffect } from 'react';
import './TripList.css'; 

const TripList = () => {
  const [trips, setTrips] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      const response = await fetch('/trips');
      const data = await response.json();
      if (response.ok) {
        setTrips(data);
      } else {
        setError('Error fetching trips');
      }
    } catch (error) {
      setError('Error fetching trips');
      console.error('Error fetching trips:', error);
    }
  };

  return (
    <div className="trip-list-container">
      <h2>List of Trips</h2>
      {error && <p className="error-message">{error}</p>}
      <div className="trip-items">
        {trips.map((trip) => (
          <div className="trip-item" key={trip.id}>
            <h3>{trip.destination}</h3>            
            <p>name: {trip.name}</p>
            <p>Start Date: {trip.start_date}</p>
            <p>End Date: {trip.end_date}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TripList;
