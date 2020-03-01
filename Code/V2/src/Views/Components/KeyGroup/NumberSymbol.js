import React, { Component } from 'react';
import {GridData} from "../Grid/Data";
import {createDefaultButtonData} from "../Grid/Button/Data";
import Grid from "../Grid";

/**
 * A keyboard for typing numbers, punctuation & standard symbols.
 */
class NumberSymbol extends Component {

    constructor(props) {
        super(props);
        this.rowSize = 5;
        this.colSize = 6;
        let buttonData = this.buildButtonData();
        this.gridData = new GridData(this.rowSize, this.colSize, buttonData);
    }

    buildButtonData() {
        let chars = [
            '1', '2', '3', '4', '5', '6',
            '7', '8', '9', '0', '#', '~',
            '\'', '\"', ':', ';', '?', '!',
            '@', '#', '$', '%', '&', '*',
            '(', ')', '+', '-', '=', '/'
        ];

        return createDefaultButtonData(chars);
    }

    render() {
        return (<Grid gridData={this.gridData} />);
    }
}

export default NumberSymbol;
