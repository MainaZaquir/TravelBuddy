import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';

import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import Profile from './components/Profile';
import Settings from './components/Settings';
import TripList from './components/TripList';
import TripDetails from './components/TripDetails';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
        <Switch>
          <Route path="/login" component={LoginForm} />
          <Route path="/signup" component={SignupForm} />
          <Route path="/profile" component={Profile} />
          <Route path="/settings" component={Settings} />
          <Route path="/trips" component={TripList} />
          <Route path="/trip/:id" component={TripDetails} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
