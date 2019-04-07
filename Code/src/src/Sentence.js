import React, { Component } from 'react';
import Letters from './components/LetterComponent';
import Numbers from './components/NumberComponent';
import Emojis from './components/EmojiComponent';

class Sentence extends React.Component {
	

	
  render(){
    return (
      <div>
        <h3>How about a whole sentence?</h3>
		<h3>Try: "I am typing with my mind."</h3>
		<input type="text" className="display" readOnly></input>
		<Letters />
		<button className="option">.</button>
		<button onClick={this.handleNumClick} className="option">0</button>
        <button onClick={this.handleEmojiClick} className="option">:)</button>
		<button className="option">&crarr;</button>
        <button className="option">&#8678;</button>
		<button onClick={this.props.sentenceHandler}>Continue</button>
		
      </div>
    )
  }
}

export default Sentence;