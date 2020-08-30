import React from 'react';
import styled from 'styled-components';
import logo from './logo.svg';
import { Counter } from './features/counter/Counter';
import { Key, KeyProps } from './components/Key';
import { KeyType, KeyStatus } from './types';
import { KeyGroup } from './components/KeyGroup';
import theme from './themes';
import './App.css';

function App() {
	const data: KeyProps[][] = [
		[
			{
				children: 'A',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
			{
				children: 'B',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
			{
				children: 'C',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
			{
				children: 'D',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
			{
				children: 'E',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
			{
				children: 'F',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
		],
		[
			{
				children: 'G',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
			{
				children: 'H',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
			{
				children: '----',
				status: KeyStatus.NEUTRAL,
				width: 2,
			},
			undefined,
			{
				children: 'I',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
			{
				children: 'J',
				status: KeyStatus.NEUTRAL,
				width: 1,
			},
		],
	];
	return (
		<div style={{ backgroundColor: theme.screen.color.background }}>
			<KeyGroup data={data} colCount={6} rowCount={3}></KeyGroup>
		</div>
	);
}

export default App;
