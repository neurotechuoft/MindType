import React, { Component } from 'react';

class Final extends React.Component {
	

  render(){
	  
	
	  
    return (
      <div className="instructionScreen">
        <h3 className="mindTypeColorText">Congratulations! You're now ready to use MindType!</h3>
		
		<button className="goToMindType" onClick={this.props.finalHandler}>Go to MindType</button>
		
      </div>
    )
  }
}

export default Final;