import {isRequired,
    isPositiveInteger,
    isFunction,
    isArray} from './ValueTypes';

/**
 * Creates ButtonData objects for each item in content,
 * with the default values of ButtonData.
 *
 * @param content - An array of the content of buttons.
 * @returns {[]} - An array of corresponding ButtonData objects.
 */
function createDefaultButtonData(content) {
    let items = [];
    for (let i=0; i<content.length; i++) {
        items[i] = new ButtonData(content[i], null, 1);
        //console.table(items[i]);
    }
    return items;
}

/**
 * Class For A Particular Button's Data
 */
class ButtonData {

    /**
     * @param content - The content (a.k.a. value) of the button.
     * @param onClick - The onClick function of the button. Optional.
     * @param width - The width of the button (a positive integer). Optional.
     *                If not specified, defaults to 1.
     */
    constructor(content, onClick, width) {
        this.typeCheckConstructor(content, onClick, width);
        this.content = content;
        this.onClick = onClick;
        this.width = (width === null) ? 1 : width;
    }

    typeCheckConstructor(content, onClick, width) {
        isRequired('content', content);
        if (onClick !== null) {
            isFunction('onClick', onClick);
        }
        if (width !== null) {
            isPositiveInteger('width', width);
        }
    }

    getContent() {
        return this.content;
    }

    setContent(content) {
        this.content = content;
    }

    getWidth() {
        return this.width;
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
     * @param buttonData - An array of ButtonData objects for each button.
     *                  The buttons and their width should perfectly fit into
     *                  'rowSize' many rows of size 'colSize'.
     */
    constructor(rowSize, colSize, buttonData) {
        this.typeCheckConstructor(rowSize, colSize, buttonData);
        this.rowSize = rowSize;
        this.colSize = colSize;
        this.buttonData = buttonData;
        this.getRowSize = this.getRowSize.bind(this);
        this.getColSize = this.getColSize.bind(this);
        this.getButtonData = this.getButtonData.bind(this);
    }

    /**
     * Validates the types of the constructor's parameters.
     */
    typeCheckConstructor(rowSize, colSize, buttonData) {

        /* CHECK PARAMETER TYPES */

        isPositiveInteger('rowSize', rowSize);
        isPositiveInteger('colSize', colSize);
        isArray('buttonData', buttonData);

        /* CHECK PARAMETER DETAILS */

        // Verify that each row has an appropriate size.
        // Also, build-up 'actualSize' value for later.

        let actualSize = 0;
        let currRowSize = 0;
        for (let i=0; i<buttonData.length; i++) {
            let newWidth = buttonData[i].getWidth();
            currRowSize += newWidth;
            if (currRowSize > colSize) {
                throw new Error('Row has invalid size. It surpasses column size. \n \n' +
                    'Expected Size (rowSize): ' + rowSize + '\n' +
                    'Current Size (counting through row): ' + currRowSize + '\n' +
                    'Button Content currently being placed: ' + buttonData[i].getContent()
                );
            } else if (currRowSize === colSize) {
                currRowSize = 0;
            }
            actualSize += newWidth;
        }
        if (currRowSize !== 0 && currRowSize !== rowSize) {
            throw new Error('Final row has invalid size. It is less than the column size.' +
                '\n \n' +
                'Expected Size (rowSize): ' + rowSize + '\n' +
                'Current Size (counting through row): ' + currRowSize
            );
        }

        // Verify that the overall button count (adjusted by width)
        // is equal to the expected size of the grid.

        let expectedSize = rowSize * colSize;
        if (expectedSize !== actualSize) {
            throw new Error('buttonData has invalid size. \n \n' +
                'Expected (from rowSize * colSize): ' + expectedSize + ' \n' +
                'Actual (from counting button sizes): ' + actualSize);
        }
    }

    getRowSize() {
        return this.rowSize;
    }

    getColSize() {
        return this.colSize;
    }

    getButtonData() {
        return this.buttonData;
    }
}

export {createDefaultButtonData, ButtonData, GridData};
