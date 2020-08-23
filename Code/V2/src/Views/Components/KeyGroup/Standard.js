import React, { Component } from 'react';
import {GridData} from "../Grid/Data";
import {ButtonData, createDefaultButtonData} from "../Grid/Button/Data";
import Grid from "../Grid";
import delete_btn from '../../Assets/delete.png';
import shift_btn from '../../Assets/shift.png';

/**
 * A standard key group for typing text, which contains:
 * - alphabet
 * - shift button
 * - backspace button
 */
class Standard extends Component {

    constructor(props) {
        super(props);
        this.rowSize = 5;
        this.colSize = 6;
        let buttonData = this.buildButtonData();
        this.gridData = new GridData(this.rowSize, this.colSize, buttonData);
    }

    buildButtonData() {

        let buttonData;

        // Alphabet
        let chars = [
            'a', 'b', 'c', 'd', 'e', 'f',
            'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x',
            'y', 'z'
        ];
        buttonData = createDefaultButtonData(chars);

        // Space Bar
        buttonData.push(new ButtonData('_', null, 2));

        // Shift & Backspace
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

export default Standard;
