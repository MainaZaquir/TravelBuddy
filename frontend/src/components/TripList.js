import React, { useState, useEffect } from 'react';

const TripList = () => {
  const [trips, setTrips] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      const response = await fetch('your-backend-trips-endpoint');
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
    <div>
      <h2>List of Trips</h2>
      {error && <p>{error}</p>}
      <div>
        {trips.map((trip) => (
          <div key={trip.id}>
            <h3>{trip.destination}</h3>
            <p>Dates: {trip.dates}</p>
            <p>Description: {trip.description}</p>
            <p>Duration: {trip.duration}</p>
            <p>Price: {trip.price}</p>
            <p>Available Seats: {trip.availableSeats}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TripList;
