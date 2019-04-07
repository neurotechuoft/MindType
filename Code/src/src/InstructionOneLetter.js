import React, { Component } from 'react';
import TwoByTwo from './TwoByTwo';

class InstructionOneLetter extends React.Component {
	

	
  render(){
	  
	
    return (
      <div className="twoByTwo">
        <h2>Try to type the letter 'b'</h2>
		<input type="text" className="displayWide" readOnly></input>
		<TwoByTwo />
		<button onClick={this.props.instructionOneLetterHandler}>Continue</button>
      </div>
    )
  }
}

export default InstructionOneLetter;
