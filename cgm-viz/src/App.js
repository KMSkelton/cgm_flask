import React, { Component } from 'react';

import Viz from './containers/Viz/Viz';

const baseURL = "http://localhost:5000"

class App extends Component {
  componentDidMount() {
    fetch(baseURL + '/devices/')
    .then(response => response.json())
    .then(json => this.setState({ devices: json }))
    .then(console.log("devices?", this.state))
  }
  
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Welcome to CGM Viz</h1>
        </header>
        <p className="App-intro">
          MVP for CGMVIZ frontend is to display Dexcom G5 glucose monitor data as raw numbers.
        </p>
        <Viz />
      </div>
    );
  }
}

export default App;
