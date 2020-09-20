import React, { SyntheticEvent, useMemo } from 'react';
import styled from 'styled-components';
import { KeyType, KeyStatus } from '../types';
import theme, { KeyTheme, KeyStatusColor } from '../themes/index';

export interface KeyProps {
    children: any;
    type?: KeyType;
    status: KeyStatus;
    width: number;
    row?: number;
    col?: number;
}

export const Key = (props: KeyProps) => {
    const { children, type = KeyType.TEXT, status, width, row, col } = props;

    const keyTheme: KeyTheme = useMemo(() => theme.key[type], [type]);

    const fontFamily: string = keyTheme.font;

    const keyStatusColor: KeyStatusColor = useMemo(() => keyTheme.color[status], [
        keyTheme,
        status,
    ]);

    let clickEvent = function (e: SyntheticEvent) {
        console.log(children);
    };

    return (
        <StyledButton
            onClick={clickEvent}
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
    row?: number;
    col?: number;
}

const StyledButton = styled.button<StyledButtonProps>`
    font-family: ${(props) => props.fontFamily};
    font-size: 1.2em;
    color: ${(props) => props.textColor};
    margin: 0.05em;
    padding: 0.25em 0.5em;
    background: ${(props) => props.backgroundColor};
    border: 2px solid ${(props) => props.backgroundColor};
    ${(props) => (props.col || props.col == 0) && `grid-column: ${props.col + 1} / ${props.col + 1 + props.width};`}
    ${(props) => (props.row || props.row == 0) && `grid-row: ${props.row + 1} / ${props.row + 2};`}
`;
