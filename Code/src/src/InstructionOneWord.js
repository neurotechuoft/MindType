import React, { Component } from 'react';
import TwoByTwo from './TwoByTwo';

class InstructionOneWord extends React.Component {
	

	
  render(){
	  
	
    return (
	<div className="instructionScreen">
      <div className="twoByTwo">
        <h3>Great! Now try the world "cab"</h3>
		<input type="text" className="displayWide" readOnly></input>
		<TwoByTwo />
		<button onClick={this.props.instructionOneWordHandler}>Continue</button>
      </div>
	</div>
    )
  }
}

export default InstructionOneWord;
