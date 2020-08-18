import React from 'react';
import styled from 'styled-components';
import theme from '../themes/index';

const Key = (props) => {
        const {children, status, roundTopLeft, roundTopRight, roundBottomLeft, roundBottomRight} = props;
        const keyColor = theme.key[status];

        return (
            <Button 
                keyColor={keyColor} 
                roundTopLeft={roundTopLeft}
                roundTopRight={roundTopRight} 
                roundBottomLeft={roundBottomLeft}
                roundBottomRight={roundBottomRight}
            >
                {children}
            </Button>
        );
};

export default Key;

const rounded = '8px';
const unrounded = '0px'; 

const Button = styled.button`
        font-size: 1em;
        color: ${theme.key.script};
        margin: 0.25em;
        padding: 0.25 0.5em;
        background: ${props => props.keyColor};
        border-radius: 
                    ${props => props.roundTopLeft ? rounded: unrounded} 
                    ${props => props.roundTopRight ? rounded : unrounded} 
                    ${props => props.roundBottomRight ? rounded : unrounded} 
                    ${props => props.roundBottomLeft ? rounded : unrounded};
        border: 2px solid ${props => props.keyColor};
         `;
