import React, { Component } from 'react';
import io from "socket.io-client";
import './App.css';
import './EntrySizes.css';

import TwoByTwo from './TwoByTwo';
import { getFlashingPause, getNextInstrPause, startNextInstrPause } from './helpers/intervals';

// Getting rows
const row1 = document.getElementsByClassName('row1');
const row2 = document.getElementsByClassName('row2');
const rows = [row1, row2];

// Getting Columns
const col1 = document.getElementsByClassName('col1');
const col2 = document.getElementsByClassName('col2');
const cols = [col1, col2];

// Keeping track of rows
let prev = rows[0];

// Selected letter
let selectedKey = null;

// Shuffled rows & cols
let row_index = 0;
let col_index = 0; 
let shuffle_rows = [row1, row2];
let shuffle_cols = [col1, col2];

// Sockets
const nlp_socket = io('http://34.73.165.89:8001'); // Socket to connect to NLP Service.
const robot_socket = io('http://localhost:8003'); // Socket to connect to RobotJS
const FLASHING_PAUSE = getFlashingPause();

class InstructionOneWord extends React.Component {
	
	constructor(props) {
    super(props);
    this.state = { 
      statement: '',
      display: 'letters', 
      displayText: '', 
      interval : null,
      lettersFound : 0,
      rowFound : false,
      colFound : false,
    };
    this.handleNumClick = this.handleNumClick.bind(this);
    this.handleEmojiClick = this.handleEmojiClick.bind(this);
    this.handleLetterClick = this.handleLetterClick.bind(this);
    this.writePhrase = this.writePhrase.bind(this);
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

  resetKey(key) {
    if (key != null) {
      key.classList.add("entryTwo");
      key.classList.remove("selectedTwo");
      key.classList.remove("chosenTwo");
    }
  }

  keyChosen(key) {
    if (key != null) {
      key.classList.add("chosenTwo");
    }
  }

  // Shuffling rows & columns
  shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    } 
  }

  writePhrase() {
    const {statement, interval, lettersFound, rowFound, colFound, displayText} = this.state;
    
    if (lettersFound === statement.length) {
      clearInterval(interval);
      setTimeout(this.props.instructionOneWordHandler, getNextInstrPause());
    } else {
      for (let j = 0; j < prev.length; j++) {
        this.resetKey(prev[j]);
      }
      // Reset selected key
      if (selectedKey != null) {
        this.resetKey(selectedKey);
      }

      // Row & column selector
      let rc;

      if (!(row_index == 2 && col_index == 2)) {
        if (row_index == 2) rc = 2;
        else if (col_index == 2) rc = 1;
        else rc = Math.floor((Math.random() * 2) + 1);
      }

      // Rows
      if (rc === 1) {
        const row = shuffle_rows[row_index++];
        prev = row;

        for (let j = 0; j < row.length; j++) {
          row[j].classList.remove("entryTwo");
          row[j].classList.add("selectedTwo");
          
          if (row[j].innerHTML === statement[lettersFound] || (row[j].innerHTML === "____" && statement[lettersFound] === " ")) {
            if (colFound) {
              selectedKey = row[j];
            }
            // Set row found 
            this.setState({rowFound : true})
          }
        }
      } 
      // Columns
      else {
        const col = shuffle_cols[col_index++];
        prev = col;

        for (let j = 0; j < col.length; j++) {
          col[j].classList.remove("entryTwo");
          col[j].classList.add("selectedTwo");
          
          // Found letter in column
          if (col[j].innerHTML === statement[lettersFound] || (col[j].innerHTML === "____" && statement[lettersFound] === " ")) {
            if (rowFound) {
              selectedKey = col[j];
            }
            // Set column found 
            this.setState({colFound : true})
          }
        }
      }

      // After all 2 rows and all 2 columns have been flashed, determine letter 
      if (row_index == 2 && col_index == 2) {
        // Reset indices
        row_index = 0;
        col_index = 0;
        this.shuffle(shuffle_rows);
        this.shuffle(shuffle_cols);
        
        this.keyChosen(selectedKey);

        const newDisplay = displayText + statement[lettersFound];
        this.setState({rowFound : false, colFound : false, 
        displayText : newDisplay, lettersFound : lettersFound + 1});
        
        // Emitting an event to the socket to type letter.
        robot_socket.emit('typing', statement[lettersFound]);
        // Emitting an event to the socket to recieve word predictions.
        nlp_socket.emit("autocomplete", newDisplay, this.handlePredictions);

      }
    }
  }
      
  componentDidMount() {
    const statement = "cab";
    setTimeout(
      function() {
        const interval = setInterval(this.writePhrase, FLASHING_PAUSE);
        this.setState({interval, statement});
      }
      .bind(this),
      startNextInstrPause()
    );
    
  }

  render(){
    return (
	  <div className="instructionScreen">
		<div className="upperTextDiv">
      <h3 className="mindTypeColorText oneWord">Great! How about a word?<br />Try: "cab"</h3>
		</div>
		<div className="keysContainer">
		  <input type="text" className="display" value={this.state.displayText} readOnly></input>
		  <TwoByTwo />
		</div>
	</div>
    )
  }
}

export default InstructionOneWord;
