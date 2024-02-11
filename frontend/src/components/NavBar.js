import React from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css'; 

const Navbar = () => {
  return (
    <div id='navbar'>
      <h1 className='heading'>Travel Buddy</h1>
      <Link to="/login">Login</Link> 
      <Link to="/signup">Signup</Link>  
      <Link to="/profile">Profile</Link> 
      <Link to="/settings">Settings</Link>  
      <Link to="/trips">Trips</Link>
    </div>
  );
}

export default Navbar;
