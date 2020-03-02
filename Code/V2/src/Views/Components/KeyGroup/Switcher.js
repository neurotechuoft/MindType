import React, { Component } from 'react';
import {GridData} from "../Grid/Data";
import {createDefaultButtonData} from "../Grid/Button/Data";
import Grid from "../Grid";
import return_btn from '../../Assets/return.png';
import {isRequired} from "../Grid/PropTypes";

/**
 * A variable common key group, which allows for switching screens.
 * Dimensions: 1 row, 6 columns
 *
 * Layout of Buttons:
 * (switch1) (switch2) . , ? return
 */
class Switcher extends Component {

    static propTypes = {
        switch1(props, propName, component) {
            isRequired(props, propName);
            if (!(props[propName] instanceof GridData)) {
                throw new Error(propName + ' is not a GridData object');
            }
            if (!(props[propName].getWidth() == 1)) {
                throw new Error(propName + '\'s width must be 1');
            }
        },
        switch2(props, propName, component) {
            isRequired(props, propName);
            if (!(props[propName] instanceof GridData)) {
                throw new Error(propName + ' is not a GridData object');
            }
            if (!(props[propName].getWidth() == 1)) {
                throw new Error(propName + '\'s width must be 1');
            }
        }
    };

    constructor(props) {
        super(props);
        this.rowSize = 1;
        this.colSize = 6;
        let buttonData = this.buildButtonData();
        this.gridData = new GridData(this.rowSize, this.colSize, buttonData);
    }

    buildButtonData() {
        let {switch1, switch2} = this.props;

        let buttonData = [];

        // VARIABLE BUTTONS
        // Switcher Button 1
        buttonData.push(switch1);
        // Switcher Button 2
        buttonData.push(switch2);

        // STANDARD BUTTONS
        let chars = [
            '.',
            ',',
            '?',
            (<img src={return_btn} className="return-img" />)
        ];
        let charsData = createDefaultButtonData(chars);
        buttonData = buttonData.concat(charsData);

        return buttonData;
    }

    render() {
        return (<Grid gridData={this.gridData} />);
    }
}

export default Switcher;
