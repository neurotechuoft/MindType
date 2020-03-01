import React, {Component} from 'react';
import {VIEWS} from './Constants';
import Letters from "../Views/Letters";

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
            return (<Letters />);
        }
        return "";
    }
}

export default Presenter;
