import React, { Component } from 'react';
import Numbers from './NumbersSmall';

class NumberSwitch extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText smallerText">Now you can select 'abc' to return to the letter keyboard.</h3>
		<input type="text" className="displayInstruction" readOnly></input>
		<Numbers />
		<button className="optionSmall bottomLeft leftMost">.</button>
		<button onClick={this.handleLetterClick} className="optionSmall">abc</button>
        <button onClick={this.handleEmojiClick} className="optionSmall">:)</button>
		<button className="optionSmall">&crarr;</button>
        <button className="optionSmall bottomRight">&#8678;</button>
		<button onClick={this.props.numberSwitchHandler}>Continue</button>
		
      </div>
    )
  }
}

export default NumberSwitch;