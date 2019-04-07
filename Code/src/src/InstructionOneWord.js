import React, { Component } from 'react';
import TwoByTwo from './TwoByTwo';

class InstructionOneWord extends React.Component {
	

	
  render(){
	  
	
    return (
      <div className="twoByTwo">
        <h2>Great! Now try the world "cab"</h2>
		<input type="text" className="displayWide" readOnly></input>
		<TwoByTwo />
		<button onClick={this.props.instructionOneWordHandler}>Continue</button>
      </div>
    )
  }
}

export default InstructionOneWord;
