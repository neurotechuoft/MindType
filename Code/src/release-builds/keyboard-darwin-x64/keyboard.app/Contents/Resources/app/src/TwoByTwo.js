import React, { Component } from 'react';

class TwoByTwo extends React.Component {
	
  render(){
    return (
      <div className="twoByTwo">
			
			<button className="entryTwo topLeft row1 col1">a</button>
            <button className="entryTwo topRight row1 col2">b</button>
			<br />
            <button className="entryTwo bottomLeft row1 col3">c</button>
            <button className="entryTwo bottomRight row1 col4">d</button>
      </div>
    )
  }
}

export default TwoByTwo;
