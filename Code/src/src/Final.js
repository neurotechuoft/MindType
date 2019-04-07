import React, { Component } from 'react';

class Final extends React.Component {
	

  render(){
    return (
      <div>
        <h3>Congratulations! You're now ready to use MindType!</h3>
		
		<button onClick={this.props.finalHandler}>Go to MindType</button>
		
      </div>
    )
  }
}

export default Final;