import {isRequired,
    isPositiveInteger,
    isNonNegativeInteger,
    isFunction,
    isArrayOfValidLength} from './ValueTypes';

/**
 * Class For A Particular Button's Data
 */
class ButtonData {

    /**
     * @param content - The content (a.k.a. value) of the button.
     * @param onClick - The onClick function of the button. Optional.
     */
    constructor(content, onClick) {
        this.typeCheckContructor(content, onClick);
        this.content = content;
        this.onClick = onClick;
    }

    typeCheckContructor(content, onClick) {
        isRequired('content', content);
        if (onClick !== null) {
            isFunction('onClick', onClick);
        }
    }

    getContent() {
        return this.content;
    }

    setContent(content) {
        this.content = content;
    }

    getOnClick() {
        return this.onClick;
    }

    setOnClick(onClick) {
        this.onClick = onClick;
    }

}


/**
 * Class For Data To Be Injected Into Grid.
 */
class GridData {

    /**
     * @param rowSize - A positive integer for the number of rows in the grid.
     * @param colSize - A positive integer for the number of cols in the grid.
     * @param contents - An array for the contents of each button. Length: rowSize * colSize.
     * @param onClicks - An array for the onClick functions of each button. Null or Length: rowSize * colSize.
     */
    constructor(rowSize, colSize, contents, onClicks) {
        this.typeCheckConstructor(rowSize, colSize, contents, onClicks);
        this.initializeValues(rowSize, colSize, contents, onClicks);
    }

    /**
     * Validates the types of the constructor's parameters.
     */
    typeCheckConstructor(rowSize, colSize, contents, onClicks) {

        isPositiveInteger('rowSize', rowSize);
        isPositiveInteger('colSize', colSize);

        let expectedLength = rowSize * colSize;
        isArrayOfValidLength('contents', contents, expectedLength);
        if (onClicks !== null) {
            isArrayOfValidLength('onClicks', onClicks, expectedLength);
        }

    }

    /**
     * Initializes the object for the constructor.
     */
    initializeValues(rowSize, colSize, contents, onClicks) {
        this.rowSize = rowSize;
        this.colSize = colSize;
        let size = rowSize * colSize;
        for (let i=0; i<size; i++) {
            this.buttons = new ButtonData(contents[i],
                onClicks ? onClicks[i] : null);
        }
    }

    /**
     * Set the onClick function of a particular button.
     *
     * All indexing of the button's position begins at 0.
     *
     * @param onClick - The onClick function of the button.
     * @param row - A non-negative integer representing the row index of the button.
     * @param col - A non-negative integer representing the col index of the button.
     */
    setOnClick(onClick, row, col) {
        isNonNegativeInteger(row);
        isNonNegativeInteger(col);
        let index = (row*this.colSize) + col;
        this.onClicks[index] = onClick;
    }

    /**
     * Set the onClick function of all buttons using an ordered array,
     * which corresponds to the same left-right, up-down order that
     * English is read in.
     *
     * @param onClicks - The ordered list of onClick functions for the buttons.
     */
    setAllOnClicks(onClicks) {
        this.onClicks = onClicks;
    }

}


export {GridData};
