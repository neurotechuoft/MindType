import React, { Component } from 'react';
import styled from 'styled-components';
import { Key, KeyProps } from './Key';
import { KeyType, KeyStatus } from '../types';
import { KeyGroup } from './KeyGroup';
import theme from '../themes';
import '../App.css';
import TextBar from './TextBar';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faBackspace, faArrowAltCircleUp } from '@fortawesome/free-solid-svg-icons';

library.add(faBackspace, faArrowAltCircleUp); //allows us to reference icon images as strings

export class Keyboard extends React.Component<{}, { text: any; capitalizeNext: boolean }> {
    constructor(props: any) {
        super(props);
        this.state = {
            text: '',
            capitalizeNext: false,
        };
    }

    changeText = (keyScript: any) => {
        const old = this.state.text;

        if (typeof keyScript === 'string') {
            const letter = this.state.capitalizeNext ? keyScript.toUpperCase() : keyScript;     // letter/spacebar key
            this.setState({ text: old + letter, capitalizeNext: false });
        } else if (keyScript.props.icon == 'backspace') {                                 //backspace key
            this.setState({ text: old.substring(0, old.length - 1) });
        } else if (keyScript.props.icon == 'arrow-alt-circle-up') {                       //shift key
            this.setState({ capitalizeNext: !this.state.capitalizeNext });
        }
    };

    data: KeyProps[][] = [
        [
            {
                children: 'a',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'b',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'c',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'd',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'e',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'f',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
        ],
        [
            {
                children: 'g',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'h',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'i',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'j',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'k',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'l',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
        ],
        [
            {
                children: 'm',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'n',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'o',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'p',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'q',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'r',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
        ],
        [
            {
                children: 's',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 't',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'u',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'v',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'w',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'x',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
        ],
        [
            {
                children: 'y',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'z',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: ' ',
                status: KeyStatus.NEUTRAL,
                width: 2,
                clickHandler: this.changeText,
            },
            (undefined as unknown) as KeyProps,
            {
                children: <FontAwesomeIcon icon="arrow-alt-circle-up" size="lg" />,
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: <FontAwesomeIcon icon="backspace" size="lg" />,
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
        ],
    ];

    Wrapper = styled.div`
        display: grid;
        grid-template-columns: auto;
        grid-template-rows: auto;
        gap: 15px;
        height: 50%;
    `;

    render() {
        return (
            <this.Wrapper>
                <TextBar>{this.state.text}</TextBar>
                <KeyGroup data={this.data} colCount={6} rowCount={5} />
            </this.Wrapper>
        );
    }
}
export default Keyboard;
