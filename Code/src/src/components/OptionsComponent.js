import React, { Component } from 'react';
import delete_btn from './../assets/delete.png';
import shift_btn from './../assets/shift.png';

class Options extends Component {

  constructor(props) {
    super(props);
    this.state = { type: props.statement };
  }

  render() {
    return (
        <div>
            <button className="switch1 entry switch topLeft bottomLeft notSelected" onClick={this.handleEmojiClick}>:)</button>
            <button className="switch2 entry switch notSelected" onClick={this.handleNumClick}>&1</button>
            <button className="entry notSelected ">.</button>
            <button className="entry notSelected">,</button>
            <button className="entry notSelected">?</button>
            <button className="entry notSelected topRight bottomRight">&crarr;</button>
        </div>
    )
  }
}

export default Options;