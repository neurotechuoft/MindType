import React from "react";
import styled from "styled-components";
import logo from "./logo.svg";
import { Counter } from "./features/counter/Counter";
import { Key, KeyProps } from "./components/Key";
import { KeyType, KeyStatus } from "./types";
import { KeyGroup } from "./components/KeyGroup";
import "./App.css";

function App() {
  const data: KeyProps[][] = [
    [
      {
        children: "A",
        status: KeyStatus.FLASHED,
        width: 1,
      },
      {
        children: "B",
        status: KeyStatus.FLASHED,
        width: 1,
      },
      {
        children: "C",
        status: KeyStatus.FLASHED,
        width: 1,
      },
      {
        children: "D",
        status: KeyStatus.FLASHED,
        width: 1,
      },
      {
        children: "E",
        status: KeyStatus.FLASHED,
        width: 1,
      },
      {
        children: "F",
        status: KeyStatus.FLASHED,
        width: 1,
      },
    ],
    [
      {
        children: "G",
        status: KeyStatus.FLASHED,
        width: 1,
      },
      {
        children: "H",
        status: KeyStatus.FLASHED,
        width: 1,
      },
      {
        children: "----",
        status: KeyStatus.FLASHED,
        width: 2,
      },
        undefined,
      {
        children: "I",
        status: KeyStatus.FLASHED,
        width: 1,
      },
      {
        children: "J",
        status: KeyStatus.FLASHED,
        width: 1,
      },
    ],
  ];

  return <KeyGroup data={data} colCount={6} rowCount={2} />;
}

export default App;
