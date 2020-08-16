import React from 'react';
import styled from 'styled-components';
import theme from '../themes/index';

const Key = (props) => {
        const keyColor = theme.key[props.status];

        const Button = styled.button`
        font-size: 1em;
        color: ${theme.key.script};
        margin: 0.25em;
        padding: 0.25 0.5em;
        border-radius: 8px;   // border-radius seems to round the button's edges with larger values and sharpen with smaller
        background: ${keyColor};   
        border: 2px solid ${keyColor};
         `;

        return (<Button>{props.children}</Button>);
};

export default Key;
