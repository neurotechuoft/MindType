import React, {Component} from 'react';
import {VIEWS} from './Constants';
import TestingBuildKeyboard from "../Views/TestingBuildKeyboard";

/**
 * Presenter in MVP Architecture.
 */
class Presenter extends Component {
    constructor(props){
        super(props);
        this.state = {
            page: VIEWS.LETTERS,
        }
    }

    render() {
        if (this.state.page === VIEWS.LETTERS) {
            return (<TestingBuildKeyboard />);
        }
        return "";
    }
}

export default Presenter;
