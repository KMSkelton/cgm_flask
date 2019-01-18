import React, { Component } from 'react';

import "./Devices.css";

// const device = (props) => (
//   <div className="DeviceModel">
//     <h4>{props.deviceModel}</h4>
//     <div className="DeviceIDs">
//       <div className="DeviceManufID">{props.manufacturerID}</div>
//     </div>
//   </div>
// );

class Device extends Component {
  constructor(){
    super();
    this.state = { devices: [] };
  }

  render() {
    // const { model, manufacturerID } = this.props.device;
    return (
      <div>
        { this.state.devices.map(device => {
          return (
            <Device key={device.id} device={device} />
          )
        })}
      </div>

    )
  }
}
export default Device;
