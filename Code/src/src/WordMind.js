import React, { Component } from 'react';
import Letters from './LettersSmallWM'

class WordMind extends React.Component {
	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText">Here's the full set of letters. Let's try to type the word "mind"</h3>
		<input type="text" className="displayInstruction" readOnly></input>
		<Letters />
		<button onClick={this.props.wordMindHandler}>Continue</button>
		
      </div>
    )
  }
}

export default WordMind;