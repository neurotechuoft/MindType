import React, { Component } from 'react';
import './App.css';

import Letters from './components/LetterComponent';
import Numbers from './components/NumberComponent';
import Emojis from './components/EmojiComponent';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { display: 'letters', type: this.props.statement, displayText: this.props.displayText };
    this.handleNumClick = this.handleNumClick.bind(this);
    this.handleEmojiClick = this.handleEmojiClick.bind(this);
    this.handleLetterClick = this.handleLetterClick.bind(this);
  }

  handleNumClick() {
    this.setState({ display: 'numbers' });
  }

  handleEmojiClick() {
    this.setState({ display: 'emojis' })
  }

  handleLetterClick() {
    this.setState({ display: 'letters' });
  }


  /*
  get phrase from user
  pass phrase into app component
  for loop the phrase (function)
  pass the letter to letter function
  generate random rows and columns and highlight them
  check if letter in each row or column
  store in row selected and colulmn selected variables
  return letter to parent, put it on screen
  */

  render() {
    let element;
    let button2;
    let button3;
    if (this.state.display === 'letters') {
      element = <Letters statement={this.props.statement}/>;
      button2 = <button onClick={this.handleNumClick} className="option">0</button>
      button3 = <button onClick={this.handleEmojiClick} className="option">:)</button>
    } else if (this.state.display === 'numbers') {
      element = <Numbers />;
      button2 = <button onClick={this.handleLetterClick} className="option">abc</button>
      button3 = <button onClick={this.handleEmojiClick} className="option">:)</button>
    } else {
      element = <Emojis />;
      button2 = <button onClick={this.handleNumClick} className="option">0</button>
      button3 = <button onClick={this.handleLetterClick} className="option">abc</button>
    }


    return (
      <div>
        <input type="text" className="display" value={this.state.displayText}></input>
        <button className="resume">Resume</button>
        <div className="suggestions">
          <button className="suggestion">To</button>
          <button className="suggestion">That</button>
          <button className="suggestion">The</button>
        </div>
        {element}
        <div className="options">
          <button className="option">.</button>
          {button2}
          {button3}
          <button className="option">&crarr;</button>
          <button className="option">&#8678;</button>
        </div>
      </div>
    )
  }

}

export default App;
