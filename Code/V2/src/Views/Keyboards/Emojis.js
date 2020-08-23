import React, { Component } from 'react';
import {ButtonData} from "../Components/Grid/Button/Data";
import Emoji from "../Components/KeyGroup/Emoji";
import Switcher from "../Components/KeyGroup/Switcher";
import Interface from "./Interface";

/**
 * A Keyboard View, with key groups:
 * - emoji group
 * - common keys w/ an ability to switch views
 */
class Letters extends Component {

    buildLowerKeyGroup() {
        // TODO: add onclicks to switch to appropriate views
        let switch1 = new ButtonData("abc", null, 1);
        let switch2 = new ButtonData("&123", null, 1);
        return (<Switcher switch1={switch1} switch2={switch2} />);
    }

    render() {
        let upperKeyGroup = (<Emoji />);
        let lowerKeyGroup = this.buildLowerKeyGroup();

        return (<Interface upperKeyGroup={upperKeyGroup} lowerKeyGroup={lowerKeyGroup} />);
    }
}

export default Letters;
