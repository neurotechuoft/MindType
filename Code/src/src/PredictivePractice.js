import React, { Component } from 'react';
import Letters from './components/LetterComponent';


class PredictivePractice extends React.Component {
	

	

  render(){
	
	
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText ppText">Let's try to save some time with predictive test. Type "I am typing with my mind! 🎉"</h3>
		<input type="text" className="displayInstruction" readOnly></input>
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