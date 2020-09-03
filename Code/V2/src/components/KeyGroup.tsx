import React from "react";
import styled from "styled-components";
import Key, { KeyProps } from "./Key";
import { KeyStatus } from "../types";

interface KeyGroupProps {
  rowCount: number;
  colCount: number;
  data: KeyProps[][];
}

export const KeyGroup = (props) => {
  const { rowCount, colCount, data } = props;
  const keys = data.map((arr: Array<KeyProps>, r: number) =>
    arr
      .filter((x) => x)
      .map((item: KeyProps, c: number) => <GridKey {...item} row={r} col={c} />)
  );
  return <Wrapper>{keys}</Wrapper>;
};

const Wrapper = styled.div`
  display: grid;
  grid-template-columns: repeat(6, auto);
  grid-template-rows: repeat(5, 30px);
  gap: 2px 2px;
`;

interface GridKeyProps extends KeyProps {
  row: number;
  col: number;
}

const GridKey = styled(Key)<GridKeyProps>`
  grid-column: ${(props) => props.col + 1} / ${(props) => props.col + 1 + props.width};
  grid-row: ${(props) => props.row + 1} / ${(props) => props.row + 2};
`;
// child grid properties in GridKey not working (GridKey seems to not be a direct child of Wrapper)
