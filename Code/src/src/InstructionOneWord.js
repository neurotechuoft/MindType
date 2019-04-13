import React, { Component } from 'react';
import TwoByTwo from './TwoByTwo';

class InstructionOneWord extends React.Component {
	

	
  render(){
	  
	
    return (
	<div className="instructionScreen">
		<div className="upperTextDiv">
        <h3 className="mindTypeColorText">Great! Now try the word "cab"</h3>
		</div>
		<div className="keysContainer">
		<input type="text" className="displayInstruction" readOnly></input>
		<TwoByTwo />
		<button onClick={this.props.instructionOneWordHandler}>Continue</button>
		
      </div>
	</div>
    )
  }
}

export default InstructionOneWord;
