import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

const statement = prompt('What would you like to type?');
let displayText = '';

ReactDOM.render(<App 
statemet={statement} displayText={displayText}/>, document.getElementById('root'));

const row1 = document.getElementsByClassName('row1');
const row2 = document.getElementsByClassName('row2');
const row3 = document.getElementsByClassName('row3');
const row4 = document.getElementsByClassName('row4');
const row5 = document.getElementsByClassName('row5');
const rows = [row1, row2, row3, row4, row5];

const col1 = document.getElementsByClassName('col1');
const col2 = document.getElementsByClassName('col2');
const col3 = document.getElementsByClassName('col3');
const col4 = document.getElementsByClassName('co14');
const col5 = document.getElementsByClassName('col5');
const col6 = document.getElementsByClassName('col6');
const cols = [col1, col2, col3, col4, col5, col6];

let iteration = 0;
let rowFound = false;
let colFound = false;

let prev = rows[0];

const interval = setInterval(writePhrase, 200);
function writePhrase() {
  if (iteration === statement.length) {
    clearInterval(interval);
  } else {
    for (let j = 0; j < prev.length; j++) {
      prev[j].style.backgroundColor = '#3da8c4';
      prev[j].style.color = 'white';
    }

    const rc = Math.floor((Math.random() * 2) + 1);
    if (rc === 1) {
      const row = rows[Math.floor((Math.random() * 5))];
      prev = row;
      for (let j = 0; j < row.length; j++) {
        row[j].style.backgroundColor = 'white';
        row[j].style.color = '#3da8c4';
        if (row[j].innerHTML === statement[iteration]) {
          rowFound = true;
        }
        if (statement[iteration] === ' ' && row === row5) {
          rowFound = true;
        }
      }
    } else {
      const col = cols[Math.floor((Math.random() * 6))];
      prev = col;
      for (let j = 0; j < col.length; j++) {
        col[j].style.backgroundColor = 'white';
        col[j].style.color = '#3da8c4';
        if (col[j].innerHTML === statement[iteration]) {
          colFound = true;
        }
        if (statement[iteration] === ' ' && col === col1) {
          colFound = true;
        }
      }
    }

    if (rowFound === true && colFound === true) {
      rowFound = false;
      colFound = false;
      displayText += statement[iteration];
      document.getElementsByClassName('display')[0].value = displayText;
      iteration++;
    }
  }
}


registerServiceWorker();
