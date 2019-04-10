import React, { Component } from 'react';
import Letters from './components/LetterComponent';
import Numbers from './components/NumberComponent';
import Emojis from './components/EmojiComponent';

class EmojiSwitch extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3>Nice! Select &123 to access numbers and symbols.</h3>
		<input type="text" className="displayInstruction" readOnly></input>
		<Emojis />
		<button className="option">.</button>
		<button onClick={this.handleNumClick} className="option">0</button>
        <button onClick={this.handleLetterClick} className="option">abc</button>
		<button className="option">&crarr;</button>
        <button className="option">&#8678;</button>
		<button onClick={this.props.emojiSwitchHandler}>Continue</button>
		
      </div>
    )
  }
}

export default EmojiSwitch;