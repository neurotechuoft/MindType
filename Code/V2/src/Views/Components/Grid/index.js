import React, { Component } from 'react';
import {CLASSES} from "./Constants";
import {isRequired, isPositiveInteger, isArrayOfValidLength} from "./PropTypes";

/**
 * Creates a Grid of Buttons.
 *
 * props.rowSize: The number of rows in the grid.
 * props.colSize: The number of columns in the grid.
 * props.contents: The value of each button in the grid.
 *
 * -----------------------------------------------------
 *
 * Note: If two adjacent items in 'contents' are the same,
 * and these are found on the same row, then it
 * only creates one button for the single value.
 *
 * For instance, when given:
 *  - rowSize = 2
 *  - colSize = 4
 *  - contents = [
 *      'a', 'a', 'a', 'b',
 *      'b', 'c', 'd', 'e',
 *      'f', 'f', 'g', 'g',
 *  ]
 *
 *  The arrangement of buttons is similar to:
 *  | a         | b |
 *  | b | c | d | e |
 *  | f     | g     |
 *
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
        contents(props, propName, component) {
            isRequired(props, propName);
            isArrayOfValidLength(props, propName, props['rowSize'] * props['colSize']); // Will this fail if rowSize or colSize not provided?
        }
    };

    getButtonIndex(r, c) {
        let {colSize} = this.props;
        return r*colSize + c;
    }

    buildButton(value, row, col, width, index) {
        let defaultClasses = CLASSES.UNSELECTED;
        let allClasses = defaultClasses + " "
            + CLASSES.ROW + row + " "
            + CLASSES.COL + col + " "
            + CLASSES.WIDTH + width;
        return (<button key={"button-" + index} className={allClasses}>
                {value}
            </button>);
    }

    buildGrid() {
        let {rowSize, colSize, contents} = this.props;
        let items = [];

        /* FOR EACH ELEMENT IN CONTENTS */
        for (let r=0; r<rowSize; r++) {
            // Refer To The Row's Previous Value Navigated To
            let prevValue = null;
            let prevWidth = 1;
            for (let c=0; c<colSize; c++) {
                // Find The Current Value Navigated To
                let index = this.getButtonIndex(r, c);
                let currValue = contents[index];

                /* CONDITIONALLY ADD BUTTONS TO 'items' ARRAY */
                if (colSize === 1) { // If we have one column
                    items.push(this.buildButton(currValue, r, c, 1, index));
                } else if (c === 0) { // If we are at the beginning of a row
                    prevValue = currValue;
                } else if (c + 1 === colSize) { // If we are at the end of a row
                    if (currValue === prevValue) {
                        // Build Previous (a.k.a. Current) Button
                        prevWidth += 1;
                        let prevCol = c-prevWidth;
                        items.push(this.buildButton(prevValue, r, prevCol, prevWidth, this.getButtonIndex(r, prevCol)));
                    } else {
                        // Build Previous Button
                        let prevCol = c-prevWidth;
                        items.push(this.buildButton(prevValue, r, prevCol, prevWidth, this.getButtonIndex(r, prevCol)));
                        // Build Current Button
                        items.push(this.buildButton(currValue, r, c, 1, index));
                    }
                    // Build Line Break As Necessary
                    if (r + 1 !== rowSize) {
                        items.push(<br key={"break-after-row-" + r}/>);
                    }
                } else { // If we are in the middle of a row
                    if (currValue === prevValue) { // If the adjacent values are equal
                        prevWidth += 1;
                    } else {
                        // Build Previous Button
                        let prevCol = c-prevWidth;
                        items.push(this.buildButton(prevValue, r, prevCol, prevWidth, this.getButtonIndex(r, prevCol)));
                        // Change Previous Value
                        prevValue = currValue;
                        prevWidth = 1;
                    }
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
