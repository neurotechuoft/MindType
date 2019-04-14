import React, { Component } from 'react';
import Letters from './LettersSmall';

class LetterSwitch extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
		<div className="upperTextDiv">
        <h3 className="mindTypeColorText smallerText upText">Let's practice switching to the emoji keyboard.<br />Try: :)</h3></div>
		<div className="keysContainer">
		<input type="text" className="displayInstruction" readOnly></input>
		<Letters />
		<button className="optionSmall leftMost bottomLeft">.</button>
		<button onClick={this.handleNumClick} className="optionSmall">0</button>
        <button onClick={this.handleEmojiClick} className="optionSmall">:)</button>
		<button className="optionSmall">&crarr;</button>
        <button className="optionSmall bottomRight">&#8678;</button>
		<button onClick={this.props.letterSwitchHandler}>Continue</button>
		</div>
      </div>
    )
  }
}

export default LetterSwitch;
