import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import Device from '../../components/Devices/Devices';

class Viz extends Component {
  constructor() {
    super();
    this.state = { devices: [] }
  }

  render() {
    return (
      <div>
        <h5>VIZ</h5>
        <Device />
      </div>
    )
  }
}

export default Viz;
