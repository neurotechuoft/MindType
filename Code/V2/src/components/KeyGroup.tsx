import React from "react";
import styled from "styled-components";
import { KeyType, KeyStatus } from "../types";
import Key, { KeyData } from "./Key";

interface KeyGroupProps {
  rowCount: number;
  colCount: number;
  data: Array<KeyData | null>[];
}

export const KeyGroup = (props: KeyGroupProps) => {
  const { rowCount, colCount, data } = props;
  const keyss = data.map((arr: KeyData[], r: number) => arr.filter(x => x as KeyData));
  const keys = data.map((arr: Array<KeyData | null>, r: number) =>
    arr
      .filter((x: KeyData | null): KeyData => x as KeyData)
      .map((item: KeyData, c: number) => (
        <Key key={c + "--" + r} {...item} row={r} col={c} />
      ))
  );
  // const test = [
  //   [
  //     <GridKey
  //       key={1}
  //       width={2}
  //       row={0}
  //       col={0}
  //       type={KeyType.TEXT}
  //       status={KeyStatus.NEUTRAL}
  //     >
  //       d
  //     </GridKey>,
  //     <GridKey
  //       key={2}
  //       width={1}
  //       row={0}
  //       col={2}
  //       type={KeyType.TEXT}
  //       status={KeyStatus.NEUTRAL}
  //     >
  //       e
  //     </GridKey>,
  //   ],
  //   [
  //     <GridKey
  //       key={3}
  //       width={1}
  //       row={1}
  //       col={0}
  //       type={KeyType.TEXT}
  //       status={KeyStatus.NEUTRAL}
  //     >
  //       f
  //     </GridKey>,
  //     <GridKey
  //       key={4}
  //       width={2}
  //       row={1}
  //       col={1}
  //       type={KeyType.TEXT}
  //       status={KeyStatus.NEUTRAL}
  //     >
  //       g
  //     </GridKey>,
  //   ],
  // ];

  // const test1arr = [
  //   <GridKey
  //     width={2}
  //     row={0}
  //     col={0}
  //     type={KeyType.TEXT}
  //     status={KeyStatus.NEUTRAL}
  //   >
  //     d
  //   </GridKey>,
  //   <GridKey
  //     width={1}
  //     row={0}
  //     col={2}
  //     type={KeyType.TEXT}
  //     status={KeyStatus.NEUTRAL}
  //   >
  //     e
  //   </GridKey>,

  //   <GridKey
  //     width={1}
  //     row={1}
  //     col={0}
  //     type={KeyType.TEXT}
  //     status={KeyStatus.NEUTRAL}
  //   >
  //     f
  //   </GridKey>,
  //   <GridKey
  //     width={2}
  //     row={1}
  //     col={1}
  //     type={KeyType.TEXT}
  //     status={KeyStatus.NEUTRAL}
  //   >
  //     g
  //   </GridKey>,
  // ];
  return (
    <Wrapper rowCount={rowCount} colCount={colCount}>
      {keys}
    </Wrapper>
  );
};

//const keyss = arr.filter((x:KeyProps) => x)

const Wrapper = styled.div<wrapperProps>`
  display: grid;
  grid-template-columns: repeat(${(props) => props.colCount}, 80px);
  grid-template-rows: repeat(${(props) => props.rowCount}, 80px);
  gap: 1px 1px;
  border-radius: 25px;
  border: 2px solid lightblue;
  margin: 8px;
`;

interface wrapperProps {
  rowCount: number;
  colCount: number;
}

// interface GridKeyProps extends KeyProps {
//   row: number;
//   col: number;
// }

// const GridKey = styled(Key)<GridKeyProps>`
//   border-radius: 25px;
//   grid-column: ${(props) => props.col + 1} / span ${(props) => props.width};
//   grid-row: ${(props) => props.row + 1} / span 1;
//   ${(props) => {
//     console.log("Helooooo: ", props);
//     return "";
//   }}
// `;
// child grid properties in GridKey not working (GridKey seems to not be a direct child of Wrapper)
// need to pass grid properties to Key since GridKey is child of Key
