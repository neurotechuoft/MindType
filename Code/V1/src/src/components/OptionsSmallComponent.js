import React, { Component } from 'react';
import delete_btn from './../assets/delete.png';
import shift_btn from './../assets/shift.png';

class OptionsSmall extends Component {

  constructor(props) {
    super(props);
    this.state = { type: props.statement };
  }

  render() {
    return (
      <span>
            <button className="entry notSelected ">.</button>
            <button className="entry notSelected">,</button>
            <button className="entry notSelected">?</button>
            <button className="entry notSelected bottomRight">&crarr;</button>
      </span>
    )
  }
}

export default OptionsSmall;