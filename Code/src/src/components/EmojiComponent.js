import React, { Component } from 'react';

class Emojis extends Component {
  render(){
    return (
      <div className="userInput">
         <button className="entry">😄</button>
         <button className="entry">😌</button>
         <button className="entry">😀</button>
         <button className="entry">😍</button>
         <button className="entry">😎</button>
         <button className="entry">😡</button>
         <br />
         <button className="entry">😅</button>
         <button className="entry">😴</button>
         <button className="entry">🙄</button>
         <button className="entry">😲</button>
         <button className="entry">😋</button>
         <button className="entry">😭</button>
         <br />
         <button className="entry">😈</button>
         <button className="entry">😇</button>
         <button className="entry">🤑</button>
         <button className="entry">🤵</button>
         <button className="entry">👰</button>
         <button className="entry">🤳</button>
         <br />
         <button className="entry">🙈</button>
         <button className="entry">🙉</button>
         <button className="entry">🙊</button>
         <button className="entry">🎅</button>
         <button className="entry">❤️️</button>
         <button className="entry">💔</button>
      </div>
    )
  }
}

export default Emojis;