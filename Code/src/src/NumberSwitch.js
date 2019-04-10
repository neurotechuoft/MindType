import React, { Component } from 'react';
import Letters from './components/LetterComponent';
import Numbers from './components/NumberComponent';
import Emojis from './components/EmojiComponent';

class NumberSwitch extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3>Now you can select 'abc' to return to the letter keyboard.</h3>
		<input type="text" className="displayInstruction" readOnly></input>
		<Numbers />
		<button className="option">.</button>
		<button onClick={this.handleLetterClick} className="option">abc</button>
        <button onClick={this.handleEmojiClick} className="option">:)</button>
		<button className="option">&crarr;</button>
        <button className="option">&#8678;</button>
		<button onClick={this.props.numberSwitchHandler}>Continue</button>
		
      </div>
    )
  }
}

export default NumberSwitch;