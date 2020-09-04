import React from "react";
import { KeyData } from "./components/Key";
import { KeyStatus } from "./types";
import { KeyGroup } from "./components/KeyGroup";
import "./App.css";

function App() {
  const data: Array<KeyData | null>[] = [
    [
      {
        children: "A",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
      {
        children: "B",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
      {
        children: "C",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
      {
        children: "D",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
      {
        children: "E",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
      {
        children: "F",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
    ],
    [
      {
        children: "G",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
      {
        children: "H",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
      {
        children: "----",
        status: KeyStatus.NEUTRAL,
        width: 2,
      },
      null,
      {
        children: "I",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
      {
        children: "J",
        status: KeyStatus.NEUTRAL,
        width: 1,
      },
    ],
  ];

  return (
    <div className="App">
      <header className="App-header">
        <KeyGroup data={data} colCount={6} rowCount={5} />
      </header>
    </div>
  );
}

export default App;
