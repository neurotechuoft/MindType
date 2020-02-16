import React, { Component } from 'react';

class Numbers extends Component {
  render() {
    return (
      <div className="userInput">
        <div>
          <button className="entry row1 col1">1</button>
          <button className="entry row1 col2">2</button>
          <button className="entry row1 col3">!</button>
          <button className="entry row1 col4">@</button>
          <button className="entry row1 col5">#</button>
          <button className="entry right row1 col6">$</button>
        </div>
        <div>
          <button className="entry row2 col1">3</button>
          <button className="entry row2 col2">4</button>
          <button className="entry row2 col3">%</button>
          <button className="entry row2 col4">^</button>
          <button className="entry row2 col5">&amp;</button>
          <button className="entry right row2 col6">~</button>
          </div>
        <div>
          <button className="entry row3 col1">5</button>
          <button className="entry row3 col2">6</button>
          <button className="entry row3 col3">+</button>
          <button className="entry row3 col4">-</button>
          <button className="entry row3 col5">=</button>
          <button className="entry right row3 col6">*</button>
        </div>
        <div>
          <button className="entry row4 col1">7</button>
          <button className="entry row4 col2">8</button>
          <button className="entry row4 col3">:</button>
          <button className="entry row4 col4">;</button>
          <button className="entry row4 col5">'</button>
          <button className="entry right row4 col6">"</button>
        </div>
        <div>
          <button className="entry bottom row5 col1">9</button>
          <button className="entry bottom row5 col2">0</button>
          <button className="entry bottom row5 col3">(</button>
          <button className="entry bottom row5 col4">)</button>
          <button className="entry bottom row5 col5">/</button>
          <button className="entry right bottom row5 col6">\</button>
        </div>
      </div>
    )
  }
}

export default Numbers;