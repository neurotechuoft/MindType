import React, { useMemo } from "react";
import styled from "styled-components";
import { KeyType, KeyStatus } from "../types";
import theme, { KeyTheme, KeyStatusColor } from "../themes/index";

export interface KeyData {
  children: any;
  type?: KeyType;
  status: KeyStatus;
  width: number;
}

export interface KeyProps extends KeyData {
  row: number;
  col: number;
}

export const Key = (props: KeyProps) => {
  const { row, col, children, type = KeyType.TEXT, status, width } = props;

  const keyTheme: KeyTheme = useMemo(() => theme.key[type], [type]);

  const fontFamily: string = keyTheme.font;

  const keyStatusColor: KeyStatusColor = useMemo(() => keyTheme.color[status], [
    keyTheme,
    status,
  ]);

  return (
    <StyledButton
      fontFamily={fontFamily}
      textColor={keyStatusColor.content}
      backgroundColor={keyStatusColor.background}
      width={width}
      row={row}
      col={col}
    >
      {children}
    </StyledButton>
  );
};

export default Key;

interface StyledButtonProps {
  fontFamily: string;
  textColor: string;
  backgroundColor: string;
  width: number;
  row: number;
  col: number;
}

const StyledButton = styled.button<StyledButtonProps>`
  font-family: ${(props) => props.fontFamily};
  font-size: 1em;
  color: ${(props) => props.textColor};
  margin: 1px;
  padding: 0.25em 0.5em;
  background: ${(props) => props.backgroundColor};
  border: 2px solid ${(props) => props.backgroundColor};
  grid-column: ${(props) => props.col + 1} / span ${(props) => props.width};
  grid-row: ${(props) => props.row + 1} / span 1;
`;
