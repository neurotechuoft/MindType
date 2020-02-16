import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './containers/App';
import Start from './Start';
import registerServiceWorker from './registerServiceWorker';
import './welcome.png';
import Control from './Control';

ReactDOM.render(<Control/>, document.getElementById('root'));


registerServiceWorker();