import React, { Component } from 'react';
import TwoByTwo from './TwoByTwo';
import io from "socket.io-client";
import './App.css';
import { getRandomArray } from './helpers/shuffle';

// Getting rows
const row1 = document.getElementsByClassName('row1');
const row2 = document.getElementsByClassName('row2');
const rows = [row1, row2];

// Getting Columns
const col1 = document.getElementsByClassName('col1');
const col2 = document.getElementsByClassName('col2');
const cols = [col1, col2];

let prev = rows[0];
let curRow = 0; // Keeping track of which array index you're on for random rows.
let curCol = 0; // Keeping track of which array index you're on for random cols.

let selectedKey = null;

const nlp_socket = io('http://34.73.165.89:8001'); // Socket to connect to NLP Service.
const robot_socket = io('http://localhost:8002'); // Socket to connect to RobotJS
const FLASHING_PAUSE = 1000;


class InstructionOneLetter extends Component {
	
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
    this.handlePredictions = this.handlePredictions.bind(this);
    this.writePhrase    = this.writePhrase.bind(this);
  }

  handlePredictions(...predictions) {
    this.setState({predictions : predictions})
  }
  
  resetKey(key) {
    if (key != null) {
      key.classList.add("entry");
      key.classList.remove("selected");
      key.classList.remove("chosen");
    }
  }

  keyChosen(key) {
    if (key != null) {
      key.classList.add("chosen");
    }
  }

  writePhrase() {
    const { statement, interval, lettersFound, rowOrder, 
      colOrder, rowFound, colFound, displayText } = this.state;

    if (lettersFound === statement.length) {
      clearInterval(interval);
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

      for (let j = 0; j < row.length; j++) {
        row[j].classList.remove("entry");
        row[j].classList.add("selected");
        if (row[j].innerHTML === statement[lettersFound]) {
          if (colFound) {
            selectedKey = row[j];
            this.keyChosen(selectedKey);
          }
          const rowOrder = getRandomArray(2);
          curRow = 0;
          this.setState({rowFound : true, rowOrder});
        }
      }
      } else {
        const col = cols[colOrder[curCol]];
        prev = col;
        curCol = curCol + 1;
        
        for (let j = 0; j < col.length; j++) {
          col[j].classList.remove("entry");
          col[j].classList.add("selected");
          if (col[j].innerHTML === statement[lettersFound]) {
            if (rowFound) {
              selectedKey = col[j];
              this.keyChosen(selectedKey);
            }
            const colOrder = getRandomArray(2);
            curCol = 0;
            this.setState({colFound : true, colOrder});
          }
        }
      }

      // If a letter has been found.
      if (rowFound && colFound) {
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
    const statement = "b";
    const rowOrder = getRandomArray(2);
    const colOrder = getRandomArray(2); 
    const interval = setInterval(this.writePhrase, FLASHING_PAUSE);
    this.setState({interval, statement, rowOrder, colOrder});
  }

	
  render(){
	  
	
    return (
      <div className="instructionScreen">
      <div className="upperTextDiv">
      <h3 className="mindTypeColorText">Let's type a letter.<br />
        Try: 'b'</h3></div>

        <div className="keysContainer">
            <input type="text" className="displayInstruction" value={this.state.displayText} readOnly></input>
            <TwoByTwo />
            <button onClick={this.props.instructionOneLetterHandler}>Continue</button>
        </div>

      </div>
    )
  }
}

export default InstructionOneLetter;
