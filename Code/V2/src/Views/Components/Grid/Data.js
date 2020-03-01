import {isPositiveInteger,
    isArray} from './ValueTypes';

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

export {GridData};
