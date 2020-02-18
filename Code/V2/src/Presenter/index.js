import React, {Component} from 'react';
import {VIEWS} from './Constants';
import LetterComponent from "../Views/LetterComponent";

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
            return (<LetterComponent />);
        }
        return "";
    }
}

export default Presenter;
