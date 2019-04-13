import React, { Component } from 'react';

class Emojis extends Component {
  render(){
    return (
      <div className="userInput">
        <div>
          <button className="entry"><span role="img" aria-label="Emoji">😊</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😂</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😉</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😍</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😘</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😋</span></button>
        </div>
        <div>
          <button className="entry"><span role="img" aria-label="Emoji">😠</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😒</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😮</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😎</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😢</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">😭</span></button>
        </div>
        <div>
          <button className="entry"><span role="img" aria-label="Emoji">🙈</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">🙉</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">🙊</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">❤️</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">💔</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">🎉</span></button>
        </div>
        <div>
          <button className="entry"><span role="img" aria-label="Emoji">👋</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">✌️</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">👍</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">👎</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">👏</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">🙏</span></button>
        </div>
        <div>
          <button className="entry"><span role="img" aria-label="Emoji">⭐</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">✨</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">🔥</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">💯</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">💩</span></button>
          <button className="entry"><span role="img" aria-label="Emoji">🌈</span></button>
        </div>
      </div>
    )
  }
}

export default Emojis;