import React, { Component } from 'react';

class Emojis extends Component {
  render(){
    return (
      <div className="userInput">
        <div>
          <button className="entry row1 col1"><span role="img" aria-label="Emoji">😊</span></button>
          <button className="entry row1 col2"><span role="img" aria-label="Emoji">😂</span></button>
          <button className="entry row1 col3"><span role="img" aria-label="Emoji">😉</span></button>
          <button className="entry row1 col4"><span role="img" aria-label="Emoji">😍</span></button>
          <button className="entry row1 col5"><span role="img" aria-label="Emoji">😘</span></button>
          <button className="entry right row1 col6"><span role="img" aria-label="Emoji">😋</span></button>
        </div>
        <div>
          <button className="entry row2 col1"><span role="img" aria-label="Emoji">😠</span></button>
          <button className="entry row2 col2"><span role="img" aria-label="Emoji">😒</span></button>
          <button className="entry row2 col3"><span role="img" aria-label="Emoji">😮</span></button>
          <button className="entry row2 col4"><span role="img" aria-label="Emoji">😎</span></button>
          <button className="entry row2 col5"><span role="img" aria-label="Emoji">😢</span></button>
          <button className="entry right row2 col6"><span role="img" aria-label="Emoji">😭</span></button>
        </div>
        <div>
          <button className="entry row3 col1"><span role="img" aria-label="Emoji">🙈</span></button>
          <button className="entry row3 col2"><span role="img" aria-label="Emoji">🙉</span></button>
          <button className="entry row3 col3"><span role="img" aria-label="Emoji">🙊</span></button>
          <button className="entry row3 col4"><span role="img" aria-label="Emoji">❤️</span></button>
          <button className="entry row3 col5"><span role="img" aria-label="Emoji">💔</span></button>
          <button className="entry right row3 col6"><span role="img" aria-label="Emoji">🎉</span></button>
        </div>
        <div>
          <button className="entry row4 col1"><span role="img" aria-label="Emoji">👋</span></button>
          <button className="entry row4 col2"><span role="img" aria-label="Emoji">✌️</span></button>
          <button className="entry row4 col3"><span role="img" aria-label="Emoji">👍</span></button>
          <button className="entry row4 col4"><span role="img" aria-label="Emoji">👎</span></button>
          <button className="entry row4 col5"><span role="img" aria-label="Emoji">👏</span></button>
          <button className="entry right row4 col6"><span role="img" aria-label="Emoji">🙏</span></button>
        </div>
        <div>
          <button className="entry bottom row5 col1"><span role="img" aria-label="Emoji">⭐</span></button>
          <button className="entry bottom row5 col2"><span role="img" aria-label="Emoji">✨</span></button>
          <button className="entry bottom row5 col3"><span role="img" aria-label="Emoji">🔥</span></button>
          <button className="entry bottom row5 col4"><span role="img" aria-label="Emoji">💯</span></button>
          <button className="entry bottom row5 col5"><span role="img" aria-label="Emoji">💩</span></button>
          <button className="entry right bottom row5 col6"><span role="img" aria-label="Emoji">🌈</span></button>
        </div>
      </div>
    )
  }
}

export default Emojis;