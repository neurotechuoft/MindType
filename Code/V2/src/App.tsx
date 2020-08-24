import React from 'react';
import styled from 'styled-components';
import logo from './logo.svg';
import { Counter } from './features/counter/Counter';
import { Key } from './components/Key';
import { KeyType, KeyStatus } from './types';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <Counter />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <span>
          <span>Learn </span>
          <a
            className="App-link"
            href="https://reactjs.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            React
          </a>
          <span>, </span>
          <a
            className="App-link"
            href="https://redux.js.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Redux
          </a>
          <span>, </span>
          <a
            className="App-link"
            href="https://redux-toolkit.js.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            Redux Toolkit
          </a>
          ,<span> and </span>
          <a
            className="App-link"
            href="https://react-redux.js.org/"
            target="_blank"
            rel="noopener noreferrer"
          >
            React Redux
          </a>
        </span>
        <Row>
          <Key type={KeyType.TEXT} status={KeyStatus.NEUTRAL}>Text Neutral</Key>
          <Key type={KeyType.TEXT} status={KeyStatus.FLASHED}>Text Flashed</Key>
          <Key type={KeyType.TEXT} status={KeyStatus.SELECTED}>Text Selected</Key>
        </Row>
        <Row>
          <Key type={KeyType.NAVIGATION} status={KeyStatus.NEUTRAL}>Text Neutral</Key>
          <Key type={KeyType.NAVIGATION} status={KeyStatus.FLASHED}>Text Flashed</Key>
          <Key type={KeyType.NAVIGATION} status={KeyStatus.SELECTED}>Text Selected</Key>
        </Row>
      </header>
    </div>
  );
}

export default App;

const Row = styled.div`
    flex-direction: row
`;
