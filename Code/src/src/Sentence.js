import React, { Component } from 'react';
import Letters from './components/LetterComponent';
import Options from './components/OptionsComponent';

import io from "socket.io-client";
import './App.css';
import './EntrySizes.css';
import { getRandomArray } from './helpers/shuffle';
import { getNextInstrPause, getFlashingPause } from './helpers/intervals';
import { sendTrainingFlashEvent } from './helpers/P300Communication';


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
let curRow = 0; // Keeping track of which array index you're on for random rows.
let curCol = 0; // Keeping track of which array index you're on for random cols.

let selectedKey = null;

const nlp_socket = io('http://34.73.165.89:8001'); // Socket to connect to NLP Service.
const client_socket = io('http://localhost:8002'); // Socket to connect to P300Client.
const robot_socket = io('http://localhost:8003'); // Socket to connect to RobotJS
const FLASHING_PAUSE = getFlashingPause();

class Sentence extends React.Component {
	
	constructor(props) {
    super(props);
    this.state = { 
      statement: '',
      display: 'letters', 
      displayText: '', 
      interval : null,
      lettersFound : 0,
      rowOrder : null,
      colOrder : null,
      rowFound : false,
      colFound : false,
      predictions: ['', '', '']
    };
    this.handleNumClick = this.handleNumClick.bind(this);
    this.handleEmojiClick = this.handleEmojiClick.bind(this);
    this.handleLetterClick = this.handleLetterClick.bind(this);
    this.handlePredictions = this.handlePredictions.bind(this);
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

  handlePredictions(...predictions) {
    this.setState({predictions : predictions})
  }

  resetKey(key) {
    if (key != null) {
      key.classList.add("entrySmall");
      key.classList.remove("selectedSmall");
      key.classList.remove("chosenSmall");
    }
  }

  keyChosen(key) {
    if (key != null) {
      key.classList.add("chosenSmall");
    }
  }

  writePhrase() {
    const {statement, interval, lettersFound, rowOrder, 
      colOrder, rowFound, colFound, displayText} = this.state;
    if (lettersFound === statement.length) {
      clearInterval(interval);
      setTimeout(this.props.sentenceHandler, getNextInstrPause());
    } else {
      for (let j = 0; j < prev.length; j++) {
        this.resetKey(prev[j]);
      }
      if (selectedKey != null) {
        this.resetKey(selectedKey);
      }
      
      // making sure rows/cols don't flash if they've already been found.
      let rc;
      if (rowFound) rc = 2;
      else if (colFound) rc = 1;
      else rc = Math.floor((Math.random() * 2) + 1);
      
      if (rc === 1) {
        const row = rows[rowOrder[curRow]];
        prev = row;
        curRow = curRow + 1;

        // Handling Spaces 

        if (statement[lettersFound] === ' ' && row === rows[4]) {
          const rowOrder = getRandomArray(5);
          curRow = 0;
          this.setState({rowFound : true, rowOrder});
        }
        for (let j = 0; j < row.length; j++) {
          row[j].classList.remove("entrySmall");
          row[j].classList.add("selectedSmall");
          if (row[j].innerHTML === statement[lettersFound]) {
            if (colFound) {
              selectedKey = row[j];
              sendTrainingFlashEvent(client_socket, true);
              // row[j].classList.add("chosen");
            }
            else {
              sendTrainingFlashEvent(client_socket, false);
            }
            // numColumSelected = j;
            const rowOrder = getRandomArray(5);
            curRow = 0;
            this.setState({rowFound : true, rowOrder});
          }
        }
      } else {
        const col = cols[colOrder[curCol]];
        prev = col;
        curCol = curCol + 1;
        
        // Handling Spaces
        if (statement[lettersFound] === ' ' && col === cols[0]) {
          const colOrder = getRandomArray(6);
          curCol = 0;
          this.setState({colFound : true, colOrder});
        }

        for (let j = 0; j < col.length; j++) {
          col[j].classList.remove("entrySmall");
          col[j].classList.add("selectedSmall");
          if (col[j].innerHTML === statement[lettersFound]) {
            if (rowFound) {
              selectedKey = col[j];
              sendTrainingFlashEvent(client_socket, true);
              // col[j].classList.add("chosen");
            }
            else {
              sendTrainingFlashEvent(client_socket, false);
            }
            const colOrder = getRandomArray(6);
            curCol = 0;
            this.setState({colFound : true, colOrder});
          }
        }
      }
      // If a letter has been found.
      if (rowFound && colFound) {
        this.keyChosen(selectedKey);
        // TODO: Reset numCol and numRow to -1
        [curRow, curCol] = [0, 0];
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
    // const statement = prompt("What would you like to type?");
    const statement = "what would you like to type";
    const rowOrder = getRandomArray(5);
    const colOrder = getRandomArray(6); 
    const interval = setInterval(this.writePhrase, FLASHING_PAUSE);
    this.setState({interval, statement, rowOrder, colOrder});
  }
	

	

	
  render(){
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText smallerText">How about a whole sentence?<br/>Try: "I am typing with my mind."</h3>
        <div className="keysContainer">
          <input type="text" className="displayInstruction" readOnly></input>
          <Letters />
          <Options />
        </div>
      </div>
    )
  }
}

export default Sentence;