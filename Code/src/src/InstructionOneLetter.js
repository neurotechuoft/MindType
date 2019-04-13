import React, { Component } from 'react';
import TwoByTwo from './TwoByTwo';



class InstructionOneLetter extends React.Component {
	

	
  render(){
	  
	
    return (
	<div className="instructionScreen">
	<div className="upperTextDiv">
	<h3 className="mindTypeColorText">Let's type a letter.<br />
	Try: 'b'</h3></div>
      <div className="keysContainer">
        
		<input type="text" className="displayInstruction" readOnly></input>
		<TwoByTwo />
		<button onClick={this.props.instructionOneLetterHandler}>Continue</button>
      </div>
	 </div>
    )
  }
}

export default InstructionOneLetter;
