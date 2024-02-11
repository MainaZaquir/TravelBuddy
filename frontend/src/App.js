import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import './index.css';
import './components/LoginForm.css'

import Navbar from './components/NavBar'; 
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import Profile from './components/Profile';
import Settings from './components/Settings';
import TripList from './components/TripList';
import TripDetails from './components/TripDetails';

function App() {
  return (
    <Router>
       <div>
      <Navbar />
      <hr />  

        <Routes>
          <Route path="/" element={<LoginForm />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/signup" element={<SignupForm />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/trips" element={<TripList />} />
          <Route path="/trip/:id" element={<TripDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
