import React, { Component } from 'react';
import Emojis from './EmojisSmall';

class EmojiSwitch extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
	  <div className="upperTextDiv">
        <h3 className="mindTypeColorText smallerText upText">Nice! Select &123 to access numbers and symbols.</h3></div>
		<div className="keysContainer">
		<input type="text" className="displayInstruction" readOnly></input>
		<Emojis />
		<button className="optionSmall leftMost bottomLeft">.</button>
		<button onClick={this.handleNumClick} className="optionSmall">0</button>
        <button onClick={this.handleLetterClick} className="optionSmall">abc</button>
		<button className="optionSmall">&crarr;</button>
        <button className="optionSmall bottomRight">&#8678;</button>
		<button onClick={this.props.emojiSwitchHandler}>Continue</button>
		</div>
      </div>
    )
  }
}

export default EmojiSwitch;