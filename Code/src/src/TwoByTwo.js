import React, { Component } from 'react';

class TwoByTwo extends React.Component {
	
  render(){
    return (
      <div className="twoByTwo">
			  <div>
          <button className="entryTwo topLeft row1 col1">a</button>
          <button className="entryTwo topRight row1 col2">b</button>
        </div>
        <div>
            <button className="entryTwo bottomLeft row2 col1">c</button>
            <button className="entryTwo bottomRight row2 col2">d</button>
        </div>
      </div>
    )
  }
}

export default TwoByTwo;
