import React from "react";
import styled from "styled-components";
import Key, { KeyProps } from "./Key";
import { KeyStatus } from "../types";

type KeyGroupProps = {
  rowCount: number;
  colCount: number;
  children: any;
  //data: KeyProps[][];
};

export const KeyGroup = (props: KeyGroupProps) => {
  const { children, rowCount, colCount /*,data*/ } = props;
  /*
  const keys = data.map((arr: Array<KeyProps>, r: number) =>
    arr
      .filter((x) => x)
      .map((item: KeyProps, c: number) => <GridKey {...item} row={r} col={c} />)
  );    
  */
  return (
    <Wrapper rowCount={rowCount} colCount={colCount}>
      {children}
    </Wrapper>
  );
};

interface wrapperProps {
  rowCount: number;
  colCount: number;
}

const stile = styled.div`
  border-radius: 25px;
  border: 2px solid red;
  margin: 8px;
  z-index: 1;
`;

const Wrapper = styled.div<wrapperProps>`
  display: grid;
  grid-template-columns: repeat(${(props) => props.colCount}, 80px);
  grid-template-rows: repeat(${(props) => props.rowCount}, 80px);
  gap: 1px 1px;
  border-radius: 25px;
  border: 2px solid lightblue;
  margin: 8px;
`;

// interface GridKeyProps extends KeyProps {
//   row: number;
//   col: number;
// }

// const GridKey = styled(Key)<GridKeyProps>`
//   grid-column: ${(props) => props.col + 1} / ${(props) => props.col};
//   grid-row: ${(props) => props.row + 1} / ${(props) => props.row + 2};
// `;
// // child grid properties in GridKey not working (GridKey seems to not be a direct child of Wrapper)
