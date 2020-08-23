import React, { Component } from 'react';
import {ButtonData} from "../Components/Grid/Button/Data";
import NumberSymbol from "../Components/KeyGroup/NumberSymbol";
import Switcher from "../Components/KeyGroup/Switcher";
import smile_btn from "../Assets/smile.png"
import Interface from "./Interface";

/**
 * A Keyboard View, with key groups:
 * - numbers & standard symbol keys
 * - common keys w/ an ability to switch views
 */
class Numbers extends Component {

    buildLowerKeyGroup() {
        // TODO: add onclicks to switch to appropriate views
        let switch1 = new ButtonData((<img src={smile_btn} className="smile-img" />), null, 1);
        let switch2 = new ButtonData("abc", null, 1);
        return (<Switcher switch1={switch1} switch2={switch2} />);
    }

    render() {
        let upperKeyGroup = (<NumberSymbol />);
        let lowerKeyGroup = this.buildLowerKeyGroup();

        return (<Interface upperKeyGroup={upperKeyGroup} lowerKeyGroup={lowerKeyGroup} />);
    }
}

export default Numbers;
