import React, { Component } from 'react';
import Letters from './components/LetterComponent';
import Numbers from './components/NumberComponent';
import Emojis from './components/EmojiComponent';

class SentenceEmoji extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3>Time to combine it all! Type "I am typing with my mind! 🎉"</h3>
		<input type="text" className="displayInstruction" readOnly></input>
		<Letters />
		<button className="option">.</button>
		<button onClick={this.handleNumClick} className="option">0</button>
        <button onClick={this.handleEmojiClick} className="option">:)</button>
		<button className="option">&crarr;</button>
        <button className="option">&#8678;</button>
		<button onClick={this.props.sentenceEmojiHandler}>Continue</button>
		
      </div>
    )
  }
}

export default SentenceEmoji;