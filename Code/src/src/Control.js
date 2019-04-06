import React, { Component } from 'react';
import App from './containers/App';
import Start from './Start';
import Intro from './Intro';
import InstructionOne from './InstructionOne';
import InstructionTwo from './InstructionTwo';
import Practice from './Practice';

class Control extends React.Component {
  constructor(props) {
      super(props);
      this.state = {screenDisplay: 'start'};
	  this.loginHandler = this.loginHandler.bind(this);
	  this.signUpHandler = this.signUpHandler.bind(this);
	  this.introHandler = this.introHandler.bind(this);
	  this.instructionOneHandler = this.instructionOneHandler.bind(this);
	  this.instructionTwoHandler = this.instructionTwoHandler.bind(this);
	  this.practiceHandler = this.practiceHandler.bind(this);
    }
	
	loginHandler(){
		this.setState({screenDisplay: 'app'});
	}
	
	signUpHandler(){
		this.setState({screenDisplay: 'intro'});
	}
	
	introHandler(){
		this.setState({screenDisplay: 'instructionOne'});
	}
	
	instructionOneHandler(){
		this.setState({screenDisplay: 'instructionTwo'});
	}
	
	instructionTwoHandler(){
		this.setState({screenDisplay: 'practice'});
	}
	
	practiceHandler(){
		this.setState({screenDisplay: 'app'});
	}

render() {
  let element;
        if (this.state.screenDisplay === 'start'){
          element = <Start loginHandler = {this.loginHandler} signUpHandler = {this.signUpHandler}/>
        } else if (this.state.screenDisplay === 'app'){
          element = <App />;
        } else if (this.state.screenDisplay === 'intro'){
		  element = <Intro introHandler={this.introHandler}/>;
		} else if (this.state.screenDisplay === 'instructionOne'){
		  element = <InstructionOne instructionOneHandler={this.instructionOneHandler}/>;
		} else if (this.state.screenDisplay === 'instructionTwo'){
		  element = <InstructionTwo instructionTwoHandler={this.instructionTwoHandler}/>;
		} else if (this.state.screenDisplay === 'practice'){
		  element = <Practice practiceHandler={this.practiceHandler} />;
		}
  return (
    <div>
      {element}
    </div>
  )
}
}

export default Control;
