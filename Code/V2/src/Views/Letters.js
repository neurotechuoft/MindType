import React, { Component } from 'react';
import Grid from "./Components/Grid";
import delete_btn from './assets/delete.png';
import shift_btn from './assets/shift.png';

class Letters extends Component {

  render() {

    let rowSize = 5;
    let colSize = 6;

    let shift = (<img src={shift_btn} className="shift-img"/>);
    let del = (<img src={delete_btn} className="delete-img"/>);

    let characters = [
        'a', 'a', 'c', 'd', 'e', 'f',
        'f', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'o', 'q', 'r',
        's', 'v', 'v', 'v', 'w', 'w',
        'y', 'z', '_', '_', shift, del
    ];

    return (<Grid rowSize={rowSize} colSize={colSize} contents={characters} />);
  }
}

export default Letters;
