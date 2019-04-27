import React, { Component } from 'react';

class Letters extends Component {

  constructor(props) {
    super(props);
    this.state = { type: props.statement };
  }

  render() {
    return (
      <div className="userInput">
            <button className="entry row1 col1 topLeft">a</button>
            <button className="entry row1 col2">b</button>
            <button className="entry row1 col3">c</button>
            <button className="entry row1 col4">d</button>
            <button className="entry row1 col5">e</button>
            <button className="entry right row1 col6 topRight">f</button>
            <br />
            <button className="entry row2 col1">g</button>
            <button className="entry row2 col2">h</button>
            <button className="entry row2 col3">i</button>
            <button className="entry row2 col4">j</button>
            <button className="entry row2 col5">k</button>
            <button className="entry right row2 col6">l</button>
            <br />
            <button className="entry row3 col1">m</button>
            <button className="entry row3 col2">n</button>
            <button className="entry row3 col3">o</button>
            <button className="entry row3 col4">p</button>
            <button className="entry row3 col5">q</button>
            <button className="entry right row3 col6">r</button>
            <br />
            <button className="entry row4 col1">s</button>
            <button className="entry row4 col2">t</button>
            <button className="entry row4 col3">u</button>
            <button className="entry row4 col4">v</button>
            <button className="entry row4 col5">w</button>
            <button className="entry right row4 col6">x</button>
            <br />
            <button className="entry bottom row5 col1 bottomLeft">y</button>
            <button className="entry bottom row5 col2">z</button>
            <button className="entry bottom extra-wide row5 col3">____</button>
            <button className="entry bottom row5 col5">&#8682;</button>
            <button className="entry right bottom row5 col6 bottomRight">&#9003;</button>
      </div>
    )
  }
}

export default Letters;