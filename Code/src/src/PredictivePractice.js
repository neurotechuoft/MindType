import React, { Component } from 'react';
import Letters from './LettersSmall';


class PredictivePractice extends React.Component {
	

	

  render(){
	
	
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText smallestText predictiveText">Let's try to save some time with predictive test. Type "I am typing with my mind! 🎉"</h3>
		<div className="keysContainer">
		<input type="text" className="displayInstruction" readOnly></input>
		<Letters />
		<button className="optionSmall leftMost bottomLeft">.</button>
		<button onClick={this.handleNumClick} className="optionSmall">0</button>
        <button onClick={this.handleEmojiClick} className="optionSmall">:)</button>
		<button className="optionSmall">&crarr;</button>
        <button className="optionSmall bottomRight">&#8678;</button>
		
		<button onClick={this.props.predictiveHandler}>Continue</button>
		</div>
      </div>
    )
  }
}



export default PredictivePractice;