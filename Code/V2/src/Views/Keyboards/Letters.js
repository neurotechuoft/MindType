import React, { Component } from 'react';
import {ButtonData} from "../Components/Grid/Button/Data";
import Standard from "../Components/KeyGroup/Standard";
import Switcher from "../Components/KeyGroup/Switcher";
import smile_btn from "../assets/smile.png"
import Interface from "./Interface";

/**
 * The View Containing:
 * - input bar
 * - word prediction
 * - keys for: standard letters, space bar, shift, backspace
 * - common keys w/ an ability to switch views
 */
class Letters extends Component {

    buildLowerKeyGroup() {
        // TODO: add onclicks to switch to appropriate views
        let switch1 = new ButtonData((<img src={smile_btn} className="smile-img" />), null, 1);
        let switch2 = new ButtonData("&123", null, 1);
        return (<Switcher switch1={switch1} switch2={switch2} />);
    }

    render() {
        let upperKeyGroup = (<Standard />);
        let lowerKeyGroup = this.buildLowerKeyGroup();

        return (<Interface upperKeyGroup={upperKeyGroup} lowerKeyGroup={lowerKeyGroup} />);
    }
}

export default Letters;
