import React, { Component } from 'react';

class Numbers extends Component {
  render() {
    return (
      <div className="userInput">
      <div>
        <button className="entry topLeft">1</button>
        <button className="entry">2</button>
        <button className="entry">!</button>
        <button className="entry">@</button>
        <button className="entry">#</button>
        <button className="entry topRight">$</button>
      </div>
      <div>
        <button className="entry">3</button>
        <button className="entry">4</button>
        <button className="entry">%</button>
        <button className="entry">^</button>
        <button className="entry">&amp;</button>
        <button className="entry">~</button>
        </div>
      <div>
        <button className="entry">5</button>
        <button className="entry">6</button>
        <button className="entry">+</button>
        <button className="entry">-</button>
        <button className="entry">=</button>
        <button className="entry">*</button>
      </div>
      <div>
        <button className="entry">7</button>
        <button className="entry">8</button>
        <button className="entry">:</button>
        <button className="entry">;</button>
        <button className="entry">'</button>
        <button className="entry">"</button>
      </div>
      <div>
        <button className="entry bottomLeft">9</button>
        <button className="entry">0</button>
        <button className="entry">(</button>
        <button className="entry">)</button>
        <button className="entry">/</button>
        <button className="entry bottomRight">\</button>
      </div>
      </div>
    )
  }
}

export default Numbers;