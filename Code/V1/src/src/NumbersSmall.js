import React, { Component } from 'react';

class NumbersSmall extends Component {
  render() {
    return (
      <div className="userInput">
        <button className="entry-wide-small topLeft leftMost">0</button>
        <button className="entry-wide-small">1</button>
        <button className="entry-wide-small">2</button>
        <button className="entry-wide-small">3</button>
        <button className="entry-wide-small topRight">4</button>
        <br />
        <button className="entry-wide-small leftMost">5</button>
        <button className="entry-wide-small">6</button>
        <button className="entry-wide-small">7</button>
        <button className="entry-wide-small">8</button>
        <button className="entry-wide-small">9</button>

      </div>
    )
  }
}

export default NumbersSmall;