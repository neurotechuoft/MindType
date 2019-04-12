import React, { Component } from 'react';
import Letters from './LettersSmall';

class SentenceEmoji extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText">Time to combine it all! Type "I am typing with my mind! 🎉"</h3>
		<input type="text" className="displayInstruction" readOnly></input>
		<Letters />
		<button className="optionSmall leftMost bottomLeft">.</button>
		<button onClick={this.handleNumClick} className="optionSmall">0</button>
        <button onClick={this.handleEmojiClick} className="optionSmall">:)</button>
		<button className="optionSmall">&crarr;</button>
        <button className="optionSmall bottomRight">&#8678;</button>
		<button onClick={this.props.sentenceEmojiHandler}>Continue</button>
		
      </div>
    )
  }
}

export default SentenceEmoji;