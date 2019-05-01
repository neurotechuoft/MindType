import React, { Component } from 'react';

class TwoByTwo extends Component {
	
  render(){
    return (
      <div className="twoByTwo">
			
			<button className="entry entryTwo topLeft row1 col1">a</button>
            <button className="entry entryTwo topRight row1 col2">b</button>
			<br />
            <button className="entry entryTwo bottomLeft row2 col1">c</button>
            <button className="entry entryTwo bottomRight row2 col2">d</button>
      </div>
    )
  }
}

export default TwoByTwo;
