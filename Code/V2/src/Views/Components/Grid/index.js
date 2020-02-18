import React, { Component } from 'react';
import {CLASSES} from "./Constants";
import {isRequired, isPositiveInteger, isArrayOfValidLength} from "./PropTypes";

/**
 * Creates a Grid of Buttons.
 *
 * props.rowSize: The number of rows in the grid.
 * props.colSize: The number of columns in the grid.
 * props.values: The value of each button in the grid.
 */
class Grid extends Component {

    static propTypes = {
        rowSize(props, propName, component) {
            isRequired(props, propName);
            isPositiveInteger(props, propName);
        },
        colSize(props, propName, component) {
            isRequired(props, propName);
            isPositiveInteger(props, propName);
        },
        values(props, propName, component) {
            isRequired(props, propName);
            isArrayOfValidLength(props, propName, props['rowSize'] * props['colSize']); // Will this fail if rowSize or colSize not provided?
        }
    };

    constructor(props) {
        super(props);
        this.state = { type: props.statement };
    }

    buildButton(value, row, col, index) {
        let defaultClasses = CLASSES.UNSELECTED;
        let allClasses = defaultClasses + " "
            + CLASSES.ROW + row + " "
            + CLASSES.COL + col;
        return (<button key={"button-" + index} className={allClasses}>
                {value}
            </button>);
    }

    buildGrid() {
        let {rowSize, colSize, values} = this.props;
        let items = [];

        for (let r=0; r<rowSize; r++) {
            for (let c=0; c<colSize; c++) {
                let index = r*colSize + c;
                let currValue = values[index];
                let button = this.buildButton(currValue, r, c, index);
                items.push(button);
                if (c + 1 === colSize && rowSize + 1 !== rowSize) {
                    items.push(<br key={"break-after-row-" + r}/>);
                }
            }
        }

        return items;
    }

    render() {
        return (<div> {this.buildGrid()} </div>);
    }
}



export default Grid;
