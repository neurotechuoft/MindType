import React from 'react';
import styled from 'styled-components';
import Key, { KeyProps } from './Key';
import { KeyStatus } from '../types';

interface KeyGroupProps {
    rowCount: number;
    colCount: number;
    data: KeyProps[][];
}

export const KeyGroup = (props: KeyGroupProps) => {
    const { rowCount, colCount, data } = props;
    const keys = data.map((arr: Array<KeyProps>, r: number) =>
        arr.map((item: KeyProps, c: number) => {
            return item ? <Key {...item} row={r} col={c} /> : null;
        })
    );
    return (
        <Grid colCount={colCount} rowCount={rowCount}>
            {keys}
        </Grid>
    );
};
interface GridProps {
    colCount: number;
    rowCount: number;
}

const Grid = styled.div<GridProps>`
    display: grid;
    grid-template-columns: repeat(${(props) => props.colCount}, 80px);
    grid-template-rows: repeat(${(props) => props.rowCount}, 80px);
    gap: 1px 1px;
    border-radius: 12px; 
    grid-column: 2 / 3;
`;
