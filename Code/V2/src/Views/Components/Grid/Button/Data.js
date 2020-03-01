import {isRequired,
    isPositiveInteger,
    isFunction} from '../ValueTypes';

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

export {createDefaultButtonData, ButtonData};
