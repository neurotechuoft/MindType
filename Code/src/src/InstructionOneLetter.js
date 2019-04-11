import React, { Component } from 'react';
import TwoByTwo from './TwoByTwo';

class InstructionOneLetter extends React.Component {
	

	
  render(){
	  
	
    return (
	<div className="instructionScreen">
      <div className="twoByTwo">
        <h3 className="mindTypeColorText">Try to type the letter 'b'</h3>
		<input type="text" className="displayWideInstruction" readOnly></input>
		<TwoByTwo />
		<button onClick={this.props.instructionOneLetterHandler}>Continue</button>
      </div>
	 </div>
    )
  }
}

export default InstructionOneLetter;
