import React, { Component } from 'react';
import styled from 'styled-components';
import { Key, KeyProps } from './Key';
import { KeyType, KeyStatus } from '../types';
import { KeyGroup } from './KeyGroup';
import theme from '../themes';
import '../App.css';
import TextBar from './TextBar';

// type TextBarState = {
//     text: String;
// };

export class Keyboard extends React.Component<{}, {text: any}> {

    constructor(props) {
        super(props);
        this.state = {
            text: ''
        };
    }

    changeText = (str) => {
        const old = this.state.text;
        this.setState({text: old + str});
    }

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
                children: '_______',
                status: KeyStatus.NEUTRAL,
                width: 2,
                clickHandler: this.changeText,
            },
            (undefined as unknown) as KeyProps,
            {
                children: 'ca',
                status: KeyStatus.NEUTRAL,
                width: 1,
                clickHandler: this.changeText,
            },
            {
                children: 'ba',
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
