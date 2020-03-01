import React, { Component } from 'react';
import {KEYS} from "./Constants";
import {isRequired} from "./PropTypes";
import {GridData} from "./Data";
import Button from "./Button";

/**
 * Creates a Grid of Buttons from a GridData object.
 *
 * props.gridData: The GridData object.
 */
class Grid extends Component {

    static propTypes = {
        gridData(props, propName, component) {
            isRequired(props, propName);
            if (!(props[propName] instanceof GridData)) {
                throw new Error(propName + ' is not a GridData object');
            }
        }
    };

    getButtonIndex(row, col) {
        let {gridData} = this.props;
        let colSize = gridData.getColSize();
        return row*colSize + col;
    }


    buildButton(value, onClick, row, col, width, index) {
        return (
            <Button content={value}
                onClick={onClick}
                row={row}
                col={col}
                width={width}
                 />
        );
    }

    buildLineBreak(index) {
        return (<br key={KEYS.BREAK + index}/>);
    }

    buildGrid() {

        let {gridData} = this.props;
        let rowSize = gridData.getRowSize();
        let colSize = gridData.getColSize();
        let buttonData = gridData.getButtonData();

        let elements = []; // The elements to be placed in the grid
        let currRow = 0; // The row we have navigated to
        let currCol = 0; // The row size we have built up

        /* FOR EACH BUTTON DATA OBJECT */
        for(let i=0; i<buttonData.length; i++) {
            // 1) Build the button
            let data = buttonData[i];
            let width = data.getWidth();
            let button = this.buildButton(
                data.getContent(),
                data.getOnClick(),
                currRow,
                currCol,
                width,
                this.getButtonIndex(currRow, currCol)
            );
            elements.push(button);
            currCol += width;
            // 2) Determine if we need to build a line break
            if (currRow + 1 !== rowSize && currCol === colSize) {
                elements.push(this.buildLineBreak(currRow));
                currRow += 1;
                currCol = 0;
            }
        }

        return elements;
    }

    render() {
        return (<div> {this.buildGrid()} </div>);
    }
}

export default Grid;
