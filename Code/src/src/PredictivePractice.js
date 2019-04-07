import React, { Component } from 'react';
import Letters from './components/LetterComponent';
import Numbers from './components/NumberComponent';
import Emojis from './components/EmojiComponent';

class PredictivePractice extends React.Component {
	

  render(){
    return (
      <div>
        <h3>Let's try to save some time with predictive test.</h3>
		<h3>Type "I am typing with my mind! 🎉"</h3>
		<p>Insert predictions here</p>
		<input type="text" className="display" readOnly></input>
		<Letters />
		<button className="option">.</button>
		<button onClick={this.handleNumClick} className="option">0</button>
        <button onClick={this.handleEmojiClick} className="option">:)</button>
		<button className="option">&crarr;</button>
        <button className="option">&#8678;</button>
		<button onClick={this.props.predictiveHandler}>Continue</button>
		
      </div>
    )
  }
}

export default PredictivePractice;