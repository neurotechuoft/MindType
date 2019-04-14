import React, { Component } from 'react';
import Letters from './LettersSmallWM'

class WordMind extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText smallerText">Let's try to type a word with the full set of letters.<br />Try: "mind"</h3>
		<div className="keysContainer">
		<input type="text" className="displayInstruction" readOnly></input>
		<Letters />
		<button onClick={this.props.wordMindHandler}>Continue</button>
		</div>
      </div>
    )
  }
}

export default WordMind;