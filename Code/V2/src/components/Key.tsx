import React, { useMemo } from "react";
import styled from "styled-components";
import { KeyType, KeyStatus } from "../types";
import theme, { KeyTheme, KeyStatusColor } from "../themes/index";

export interface KeyProps {
  children: any;
  type?: KeyType;
  status: KeyStatus;
  gridColumn: string;
  gridRow: string;
}

export const Key = (props: KeyProps) => {
  const { gridRow, gridColumn, children, type = KeyType.TEXT, status } = props;

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
      gridColumn={gridColumn}
      gridRow={gridRow}
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
  gridColumn: string;
  gridRow: string;
}

const StyledButton = styled.button<StyledButtonProps>`
  font-family: ${(props) => props.fontFamily};
  font-size: 1.4em;
  color: ${(props) => props.textColor};
  margin: 1px;
  padding: 0.25em 0.5em;
  background: ${(props) => props.backgroundColor};
  border: 2px solid ${(props) => props.backgroundColor};
  grid-column: ${(props) => props.gridColumn};
  grid-row: ${(props) => props.gridRow};
`;
