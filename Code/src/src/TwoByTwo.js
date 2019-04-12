import React, { Component } from 'react';

class TwoByTwo extends React.Component {
	
  render(){
    return (
      <div >
			
			<button className="entryTwo row1 col1">a</button>
            <button className="entryTwo row1 col2">b</button>
			<br />
            <button className="entryTwo row1 col3">c</button>
            <button className="entryTwo row1 col4">d</button>
      </div>
    )
  }
}

export default TwoByTwo;
