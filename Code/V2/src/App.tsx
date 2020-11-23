import React from 'react';
import styled from 'styled-components';
import { Key, KeyProps } from './components/Key';
import { KeyType, KeyStatus } from './types';
import { KeyGroup } from './components/KeyGroup';
import theme from './themes';
import './App.css';
import Keyboard from './components/Keyboard';
import TextBar from './components/TextBar';

function App() {
    return (
        <div className="App">
            <div className="App-header">
                <Keyboard></Keyboard>
            </div>
            
        </div>
    );
}

export default App;
