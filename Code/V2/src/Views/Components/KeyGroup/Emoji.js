import React, { Component } from 'react';
import {GridData} from "../Grid/Data";
import {createDefaultButtonData} from "../Grid/Button/Data";
import Grid from "../Grid";

/**
 * A key group for typing emojis.
 */
class Emoji extends Component {

    constructor(props) {
        super(props);
        this.rowSize = 5;
        this.colSize = 6;
        let buttonData = this.buildButtonData();
        this.gridData = new GridData(this.rowSize, this.colSize, buttonData);
    }

    buildButtonData() {
        let chars = [
            '😊', '😂', '😉', '😍', '😘', '😋',
            '😠', '😒', '😮', '😎', '😢', '😭',
            '🙈', '🙉', '🙊', '❤', '💔', '🎉',
            '👋', '✌', '👍', '👎', '👏', '🙏',
            '⭐', '✨', '🔥', '💯', '💩', '🌈'
        ];

        return createDefaultButtonData(chars);
    }

    render() {
        return (<Grid gridData={this.gridData} />);
    }
}

export default Emoji;
