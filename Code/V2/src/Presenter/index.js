import React, {Component} from 'react';
import {VIEWS} from './Constants';
import App from '../Views/App';

/**
 * Presenter in MVP Architecture.
 */
class Presenter extends Component {
    constructor(props){
        super(props);
        this.state = {
            page: VIEWS.APP,
        }
    }

    render() {
        if(this.state.page === VIEWS.APP){
            return (<App/>);
        }
        return "";
    }

}

export default Presenter;
