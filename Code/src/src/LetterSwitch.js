import React, { Component } from 'react';
import Letters from './components/LetterComponent';
import Numbers from './components/NumberComponent';
import Emojis from './components/EmojiComponent';

class LetterSwitch extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText">Let's practice switching between keyboards. Select :) to access the emojis</h3>
		<input type="text" className="displayInstruction" readOnly></input>
		<Letters />
		<button className="option">.</button>
		<button onClick={this.handleNumClick} className="option">0</button>
        <button onClick={this.handleEmojiClick} className="option">:)</button>
		<button className="option">&crarr;</button>
        <button className="option">&#8678;</button>
		<button onClick={this.props.letterSwitchHandler}>Continue</button>
		
      </div>
    )
  }
}

export default LetterSwitch;
