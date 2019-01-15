import React, { Component } from 'react';
import '../App.css';

import Letters from '../components/LetterComponent';
import Numbers from '../components/NumberComponent';
import Emojis from '../components/EmojiComponent';

// Getting rows
const row1 = document.getElementsByClassName('row1');
const row2 = document.getElementsByClassName('row2');
const row3 = document.getElementsByClassName('row3');
const row4 = document.getElementsByClassName('row4');
const row5 = document.getElementsByClassName('row5');
const rows = [row1, row2, row3, row4, row5];

// Getting Columns
const col1 = document.getElementsByClassName('col1');
const col2 = document.getElementsByClassName('col2');
const col3 = document.getElementsByClassName('col3');
const col4 = document.getElementsByClassName('col4');
const col5 = document.getElementsByClassName('col5');
const col6 = document.getElementsByClassName('col6');
const cols = [col1, col2, col3, col4, col5, col6];

let prev = rows[0];

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      statement: '',
      display: 'letters', 
      displayText: '', 
      rows : rows, 
      cols : cols,
      interval : null,
      iteration : 0,
      rowFound : false,
      colFound : false
    };
    this.handleNumClick = this.handleNumClick.bind(this);
    this.handleEmojiClick = this.handleEmojiClick.bind(this);
    this.handleLetterClick = this.handleLetterClick.bind(this);
    this.writePhrase    = this.writePhrase.bind(this);
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

  writePhrase() {
    if (this.state.iteration === this.state.statement.length) {
      clearInterval(this.state.interval);
    } else {
      for (let j = 0; j < prev.length; j++) {
        prev[j].style.backgroundColor = '#3da8c4';
        prev[j].style.color = 'white';
      }
      const rc = Math.floor((Math.random() * 2) + 1);
      if (rc === 1) {
        const row = this.state.rows[Math.floor(Math.random() * 5)];
        prev = row;
        // Handling Spaces 
        if (this.state.statement[this.state.iteration] === ' ' && row === this.state.rows[4]) {
          this.setState({rowFound : true});
        }
        for (let j = 0; j < row.length; j++) {
          row[j].style.backgroundColor = 'white';
          row[j].style.color = '#3da8c4';
          if (row[j].innerHTML === this.state.statement[this.state.iteration]) {
            this.setState({rowFound : true});
          }
        }
      } else {
        const col = this.state.cols[Math.floor(Math.random() * 6)];
        prev = col;
        // Handling Spaces
        if (this.state.statement[this.state.iteration] === ' ' && col === this.state.cols[0]) {
          this.setState({colFound : true});
        }
        for (let j = 0; j < col.length; j++) {
          col[j].style.backgroundColor = 'white';
          col[j].style.color = '#3da8c4';
          if (col[j].innerHTML === this.state.statement[this.state.iteration]) {
            this.setState({colFound : true});
          }
        }
      }
      if (this.state.rowFound && this.state.colFound) {
        const displayText = this.state.displayText + this.state.statement[this.state.iteration];
        const iteration = this.state.iteration + 1;
        this.setState({rowFound : false, colFound : false, displayText, iteration});
      }
    }
  }

  componentDidMount() {
    const statement = prompt("What would you like to type?");
    const interval = setInterval(this.writePhrase, 500);
    this.setState({interval, statement});
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
      element = <Letters />;
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
        <input type="text" className="display" value={this.state.displayText} readOnly></input>
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
