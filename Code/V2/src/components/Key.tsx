import React, { useMemo } from "react";
import styled from "styled-components";
import { KeyType, KeyStatus } from "../types";
import theme, { KeyTheme, KeyStatusColor } from "../themes/index";

export interface KeyProps {
  children: any;
  type?: KeyType;
  status: KeyStatus;
  width: number;
}

export const Key = (props: KeyProps) => {
  const { children, type=KeyType.TEXT, status, width } = props;

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
}

const StyledButton = styled.button<StyledButtonProps>`
  font-family: ${(props) => props.fontFamily};
  font-size: 1em;
  color: ${(props) => props.textColor};
  margin: 0.05em;
  padding: 0.25em 0.5em;
  background: ${(props) => props.backgroundColor};
  border: 2px solid ${(props) => props.backgroundColor};
  border-radius: 8px;
`;
