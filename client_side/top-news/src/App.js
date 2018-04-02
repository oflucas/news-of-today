import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.min.js';

import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css'; // defines style

class App extends Component {
  render() {
    return (
      <div>
        <img src={logo} className="App-logo" alt="logo" />
        <div className="container">
        </div>
      </div>
    );
  }
  // S5.mp4 20:04 
}

export default App;
