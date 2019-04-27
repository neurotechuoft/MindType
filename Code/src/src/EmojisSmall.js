import React, { Component } from 'react';

class EmojisSmall extends Component {
  render(){
    return (
      <div className="userInput">
        <div>
         <button className="entry entrySmall topLeft leftMost"><span role="img" aria-label="Emoji">😊</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😂</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😉</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😍</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😘</span></button>
         <button className="entry entrySmall topRight"><span role="img" aria-label="Emoji">😋</span></button>
       </div>
       <div>
         <button className="entry entrySmall leftMost"><span role="img" aria-label="Emoji">😠</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😒</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😮</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😎</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😢</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">😭</span></button>
       </div>
       <div>
         <button className="entry entrySmall leftMost"><span role="img" aria-label="Emoji">🙈</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">🙉</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">🙊</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">❤️</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">💔</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">🎉</span></button>
       </div>
       <div>
         <button className="entry entrySmall leftMost"><span role="img" aria-label="Emoji">👋</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">✌️</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">👍</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">👎</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">👏</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">🙏</span></button>
       </div>
       <div>
         <button className="entry entrySmall leftMost"><span role="img" aria-label="Emoji">⭐</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">✨</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">🔥</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">💯</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">💩</span></button>
         <button className="entry entrySmall"><span role="img" aria-label="Emoji">🌈</span></button>
       </div>
      </div>
    )
  }
}

export default EmojisSmall;