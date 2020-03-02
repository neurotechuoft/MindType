import React, { Component } from 'react';
import PropTypes from 'prop-types';

/**
 * Enforces the Standard Format of Keyboard Views.
 *
 * A Keyboard View Contains:
 * - textfield
 * - a word prediction bar
 * - two keyboard groups
 */
class Interface extends Component {

    static propTypes = {
        upperKeyGroup: PropTypes.object,
        lowerKeyGroup: PropTypes.object
    };

    constructor(props) {
        super(props);
        this.inputBar = this.buildInputBar();
        this.wordPrediction = this.buildWordPrediction();
    }

    buildInputBar() {
        return (<input name="lettersInput" type="text" />);
    }

    buildWordPrediction() {
        return null; // TODO: make this component
    }

    render() {
        let {upperKeyGroup, lowerKeyGroup} = this.props;

        return (<div>
            {this.inputBar}
            <br/>
            {this.wordCompletion}
            <br/>
            {upperKeyGroup}
            <br/>
            {lowerKeyGroup}
            </div>);
    }
}

export default Interface;
