import React from "react";
import styled from "styled-components";
import Key from "./Key.js";
import { KeyStatus } from "../types";

const KeyGroup = (props) => {
  const { row_count, col_count } = props;
  const keyboard = Array(row_count)
    .fill(KeyStatus.NEUTRAL)
    .map((x) => Array(col_count).fill(x));
};

// const KeyGroup = styled.div`
//     display: flex;
//     flex-flow: row wrap;

const Wrapper = styled.div`
  flex-direction: column;
`;

const Row = styled.div`
  flex-direction: row;
  width: 100%;
`;

export default Row;
