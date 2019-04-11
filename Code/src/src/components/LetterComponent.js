import React, { Component } from 'react';

class Letters extends Component {

  constructor(props) {
    super(props);
    this.state = { type: props.statement };
  }

  render() {
    return (
      <div className="userInput">
            <button className="entry row1 col1">a</button>
            <button className="entry row1 col2">b</button>
            <button className="entry row1 col3">c</button>
            <button className="entry row1 col4">d</button>
            <button className="entry row1 col5">e</button>
            <button className="entry row1 col6">f</button>
            <br />
            <button className="entry row2 col1">g</button>
            <button className="entry row2 col2">h</button>
            <button className="entry row2 col3">i</button>
            <button className="entry row2 col4">j</button>
            <button className="entry row2 col5">k</button>
            <button className="entry row2 col6">l</button>
            <br />
            <button className="entry row3 col1">m</button>
            <button className="entry row3 col2">n</button>
            <button className="entry row3 col3">o</button>
            <button className="entry row3 col4">p</button>
            <button className="entry row3 col5">q</button>
            <button className="entry row3 col6">r</button>
            <br />
            <button className="entry row4 col1">s</button>
            <button className="entry row4 col2">t</button>
            <button className="entry row4 col3">u</button>
            <button className="entry row4 col4">v</button>
            <button className="entry row4 col5">w</button>
            <button className="entry row4 col6">x</button>
            <br />
            <button className="entry-extra-wide row5 col1">____</button>
            <button className="entry row5 col3">y</button>
            <button className="entry row5 col4">z</button>
            <button className="entry-extra-wide row5 col5">&uarr;</button>
      </div>
    )
  }
}

export default Letters;