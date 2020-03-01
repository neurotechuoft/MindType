import React, { Component } from 'react';
import {ButtonData} from "./Components/Grid/Button/Data";
import Standard from "./Components/Keyboard/Standard";
import Switcher from "./Components/Keyboard/Switcher";
import smile_btn from "./assets/smile.png"
import return_btn from "./assets/return.png";

class Letters extends Component {

    buildLowerKeyboard() {
        // TODO: add onclicks to switch to appropriate views
        let switch1 = new ButtonData((<img src={smile_btn} className="smile-img" />), null, 1);
        let switch2 = new ButtonData("&123", null, 1);
        return (<Switcher switch1={switch1} switch2={switch2} />);
    }

    render() {
        let inputBar = (<input name="lettersInput" type="text" />);
        let wordCompletion = null; // TODO: make this component
        let upperKeyboard = (<Standard />);
        let lowerKeyboard = this.buildLowerKeyboard();

        return (<div>
                {inputBar}
                <br/>
                {wordCompletion}
                <br/>
                {upperKeyboard}
                <br/>
                {lowerKeyboard}
            </div>);
    }
}

export default Letters;
