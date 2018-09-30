import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

var statement = prompt('What would you like to type?');
var displayText = '';

ReactDOM.render(<App 
statemet={statement} displayText={displayText}/>, document.getElementById('root'));

var row1 = document.getElementsByClassName('row1');
var row2 = document.getElementsByClassName('row2');
var row3 = document.getElementsByClassName('row3');
var row4 = document.getElementsByClassName('row4');
var row5 = document.getElementsByClassName('row5');
var rows = [row1, row2, row3, row4, row5];

var col1 = document.getElementsByClassName('col1');
var col2 = document.getElementsByClassName('col2');
var col3 = document.getElementsByClassName('col3');
var col4 = document.getElementsByClassName('co14');
var col5 = document.getElementsByClassName('col5');
var col6 = document.getElementsByClassName('col6');
var cols = [col1, col2, col3, col4, col5, col6];

var iteration = 0;
var rowFound = false;
var colFound = false;

var prev = rows[0];

var interval = setInterval(writePhrase, 200);
function writePhrase() {
  if (iteration == statement.length) {
    clearInterval(interval);
  } else {
    for (var j = 0; j < prev.length; j++) {
      prev[j].style.backgroundColor = '#3da8c4';
      prev[j].style.color = 'white';
    }

    var rc = Math.floor((Math.random() * 2) + 1);
    if (rc == 1) {
      var row = rows[Math.floor((Math.random() * 5))];
      prev = row;
      for (var j = 0; j < row.length; j++) {
        row[j].style.backgroundColor = 'white';
        row[j].style.color = '#3da8c4';
        if (row[j].innerHTML == statement[iteration]) {
          rowFound = true;
        }
        if (statement[iteration] == ' ' && row == row5) {
          rowFound = true;
        }
      }
    } else {
      var col = cols[Math.floor((Math.random() * 6))];
      prev = col;
      for (var j = 0; j < col.length; j++) {
        col[j].style.backgroundColor = 'white';
        col[j].style.color = '#3da8c4';
        if (col[j].innerHTML == statement[iteration]) {
          colFound = true;
        }
        if (statement[iteration] == ' ' && col == col1) {
          colFound = true;
        }
      }
    }

    if (rowFound == true && colFound == true) {
      rowFound = false;
      colFound = false;
      displayText += statement[iteration];
      document.getElementsByClassName('display')[0].value = displayText;
      iteration++;
    }
  }
}


registerServiceWorker();
