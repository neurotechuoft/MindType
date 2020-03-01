import React, {Component} from 'react';
import {VIEWS} from './Constants';
import Letters from "../Views/Keyboards/Letters";
import Numbers from "../Views/Keyboards/Numbers";

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
        } else if (this.state.page === VIEWS.NUMBERS) {
            return (<Numbers />);
        }
        return "";
    }
}

export default Presenter;
