import React, { Component } from 'react';
import Grid from "./Components/Grid";
import {CLASSES} from "./Components/Grid/Constants";
import delete_btn from './assets/delete.png';
import shift_btn from './assets/shift.png';

class Letters extends Component {

  render() {

    let rowSize = 4;
    let colSize = 6;

    let characters = [
        'a', 'a', 'c', 'd', 'e', 'f',
        'f', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'o', 'q', 'r',
        's', 'v', 'v', 'v', 'w', 'w'
    ];

    return (
      <div>
            <Grid rowSize={rowSize} colSize={colSize} contents={characters} />
            <br />
            <button className={CLASSES.UNSELECTED + " " + CLASSES.ROW + "4" + " " + CLASSES.COL + "0"}>y</button>
            <button className={CLASSES.UNSELECTED + " " + CLASSES.ROW + "4" + " " + CLASSES.COL + "1"}>z</button>
            <button className={CLASSES.UNSELECTED + " " + CLASSES.ROW + "4" + " " + CLASSES.COL + "2" + CLASSES.WIDTH + "0"}>____</button>
            <button className={CLASSES.UNSELECTED + " " + CLASSES.ROW + "4" + " " + CLASSES.COL + "4"}>
              <img src={shift_btn} className="shift-img"></img>
            </button>
            <button className={CLASSES.UNSELECTED + " " + CLASSES.ROW + "4" + " " + CLASSES.COL + "5"}>
              <img src={delete_btn} className="delete-img"></img>
            </button>
      </div>
    );
  }
}

export default Letters;
