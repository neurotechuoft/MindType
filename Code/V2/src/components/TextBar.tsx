import React, { useState } from 'react';
import styled from 'styled-components';
import theme from '../themes/index';
import Key from './Key';

export interface TextBarProps {
    children: any
}

export const TextBar = (props: TextBarProps) => {
    const { children } = props;

    return (
        <StyledBar
            fontFamily = {theme.inputBar.font}
            textColor = {theme.inputBar.color.text}
            backgroundColor = {theme.inputBar.color.background}
        >
            {children}
        </StyledBar>
    )
}

export default TextBar;

interface StyledBarProps {
    fontFamily: string,
    textColor: string;
    backgroundColor: string;}

const StyledBar = styled.div<StyledBarProps>`
    font-family: ${(props) => props.fontFamily};
    font-size: 1.2em;
    color: ${(props) => props.textColor};
    margin: 0.05em;
    padding: 0.25em 0.5em;
    background: ${(props) => props.backgroundColor};
    border: 2px solid ${(props) => props.backgroundColor};
    text-align: left;
    width: ${2.5 * 6}em;
`;