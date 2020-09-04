import React from "react";
import styled from "styled-components";
import { Key } from "./components/Key";
import { KeyType, KeyStatus } from "./types";
import "./App.css";
import { KeyGroup } from "./components/KeyGroup";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <KeyGroup rowCount={1} colCount={6}>
          <Key
            gridColumn={"1/ span 2"}
            gridRow={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            This
          </Key>
          <Key
            gridColumn={"3/ span 2"}
            gridRow={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            The
          </Key>
          <Key
            gridColumn={"5/ span 2"}
            gridRow={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            That
          </Key>
        </KeyGroup>

        <KeyGroup rowCount={5} colCount={6}>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            a
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"2/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            b
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"3/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            c
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"4/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            d
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"5/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            e
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"6/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            f
          </Key>
          <Key
            gridRow={"2/ span 1"}
            gridColumn={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            g
          </Key>
          <Key
            gridRow={"2/ span 1"}
            gridColumn={"2/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            h
          </Key>
          <Key
            gridRow={"2/ span 1"}
            gridColumn={"3/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            i
          </Key>
          <Key
            gridRow={"2/ span 1"}
            gridColumn={"4/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            j
          </Key>
          <Key
            gridRow={"2/ span 1"}
            gridColumn={"5/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            k
          </Key>
          <Key
            gridRow={"2/ span 1"}
            gridColumn={"6/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            l
          </Key>
          <Key
            gridRow={"3/ span 1"}
            gridColumn={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            m
          </Key>
          <Key
            gridRow={"3/ span 1"}
            gridColumn={"2/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            n
          </Key>
          <Key
            gridRow={"3/ span 1"}
            gridColumn={"3/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            o
          </Key>
          <Key
            gridRow={"3/ span 1"}
            gridColumn={"4/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            p
          </Key>
          <Key
            gridRow={"3/ span 1"}
            gridColumn={"5/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            q
          </Key>
          <Key
            gridRow={"3/ span 1"}
            gridColumn={"6/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            r
          </Key>
          <Key
            gridRow={"4/ span 1"}
            gridColumn={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            s
          </Key>
          <Key
            gridRow={"4/ span 1"}
            gridColumn={"2/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            t
          </Key>
          <Key
            gridRow={"4/ span 1"}
            gridColumn={"3/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            u
          </Key>
          <Key
            gridRow={"4/ span 1"}
            gridColumn={"4/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            v
          </Key>
          <Key
            gridRow={"4/ span 1"}
            gridColumn={"5/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            w
          </Key>
          <Key
            gridRow={"4/ span 1"}
            gridColumn={"6/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            x
          </Key>
          <Key
            gridRow={"5/ span 1"}
            gridColumn={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            y
          </Key>
          <Key
            gridRow={"5/ span 1"}
            gridColumn={"2/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            z
          </Key>
          <Key
            gridRow={"5/ span 1"}
            gridColumn={"3/ span 2"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            _____
          </Key>
          <Key
            gridRow={"5/ span 1"}
            gridColumn={"5/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            s
          </Key>
          <Key
            gridRow={"5/ span 1"}
            gridColumn={"6/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            b
          </Key>
        </KeyGroup>

        <KeyGroup rowCount={1} colCount={6}>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"1/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            s
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"2/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            n
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"3/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            .
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"4/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            ,
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"5/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            q
          </Key>
          <Key
            gridRow={"1/ span 1"}
            gridColumn={"6/ span 1"}
            type={KeyType.TEXT}
            status={KeyStatus.NEUTRAL}
          >
            b
          </Key>
        </KeyGroup>
      </header>
    </div>
  );
}

export default App;
