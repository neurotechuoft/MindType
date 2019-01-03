import React, { Component } from 'react';

class Letters extends Component {

  constructor(props) {
    super(props);
    this.state = { type: props.statement };
  }

  render() {
    let buttons = [];
    for (let i = 0; i < 26; i++) {
      const rowNum = i / 6 + 1;
      const colNum = i % 6 + 1;
      const letter = (i + 10).toString(36);
      const className = "entry row" + rowNum + " col" + colNum;
      buttons.push(<button className={className}>{letter}</button>);
      if (i !== 0 && (i+1) % 6 === 0) {
        buttons.push(<br />)
      }
    }
    return (
      <div className="userInput">
        {buttons}
      </div>
    )
  }
}

export default Letters;