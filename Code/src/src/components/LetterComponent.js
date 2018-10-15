import React, { Component } from 'react';

class Letters extends Component {

  constructor(props) {
    super(props);
    this.state = { type: props.statement };
    this.createButtons = this.createButtons.bind(this);
  }

  createButtons() {
    let buttons = [];
    for (let i = 0; i < 26; i++) {
      var rowNum = i / 6 + 1;
      var colNum = i % 6 + 1;
      var letter = (i + 10).toString(36);
      var className = "entry row" + rowNum + " col" + colNum;
      buttons.push(<button className={className}>{letter}</button>);
      if (i !== 0 && (i+1) % 6 === 0) {
        buttons.push(<br />)
      }
    }
    return buttons;
  }


  render() {
    return (
      <div className="userInput">
        {this.createButtons()}
      </div>
    )
  }
}

export default Letters;