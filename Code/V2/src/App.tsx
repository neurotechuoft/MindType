import React from 'react';
import styled from 'styled-components';
import { Key, KeyProps } from './components/Key';
import { KeyType, KeyStatus } from './types';
import { KeyGroup } from './components/KeyGroup';
import theme from './themes';
import './App.css';

function App() {
    const data: KeyProps[][] = [
        [
            {
                children: 'a',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'b',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'c',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'd',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'e',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'f',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
        ],
        [
            {
                children: 'g',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'h',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'i',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'j',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'k',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'l',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
        ],
        [
            {
                children: 'm',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'n',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'o',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'p',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'q',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'r',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
        ],
        [
            {
                children: 's',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 't',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'u',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'v',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'w',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'x',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
        ],
        [
            {
                children: 'y',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'z',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: '_______',
                status: KeyStatus.NEUTRAL,
                width: 2,
            },
            (undefined as unknown) as KeyProps,
            {
                children: 'ca',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
            {
                children: 'ba',
                status: KeyStatus.NEUTRAL,
                width: 1,
            },
        ],
    ];
    return (
        <div className="App">
            <header className="App-header">
                <KeyGroup data={data} colCount={6} rowCount={5}></KeyGroup>
            </header>
        </div>
    );
}

export default App;
