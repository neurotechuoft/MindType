import React, { Component } from 'react';
import {GridData} from "./Components/Grid/Data";
import {ButtonData, createDefaultButtonData} from "./Components/Grid/Button/Data";
import Grid from "./Components/Grid";
import delete_btn from './assets/delete.png';
import shift_btn from './assets/shift.png';

class Letters extends Component {

  constructor(props) {
    super(props);
    this.rowSize = 5;
    this.colSize = 6;
    let buttonData = this.buildButtonData();
    this.gridData = new GridData(this.rowSize, this.colSize, buttonData);
  }

    buildButtonData() {

        let buttonData = [];

        buttonData = buttonData.concat([
             new ButtonData('a', null, 2),
             new ButtonData('c', null, 1),
             new ButtonData('d', null, 3)
        ]);


        let middleCharacters = [
            'f', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x',
            'y', 'z'
        ];
        let middleData = createDefaultButtonData(middleCharacters);
        buttonData = buttonData.concat(middleData);

        buttonData.push(new ButtonData('_', null, 2));

        let shift = (<img src={shift_btn} className="shift-img"/>);
        let del = (<img src={delete_btn} className="delete-img"/>);
        let endData = createDefaultButtonData([shift, del]);
        buttonData = buttonData.concat(endData);

        return buttonData;
    }

  render() {
    return (<Grid gridData={this.gridData} />);
  }
}

export default Letters;
