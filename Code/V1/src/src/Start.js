import React, { Component } from 'react';
import SignUp from './SignUp';
import Login from './Login';
import logo from './welcome.png'

class Start extends React.Component {
  constructor(props) {
      super(props);
      this.state = {display: 'welcome'};
      this.handleLoginClick = this.handleLoginClick.bind(this);
      this.handleSignUpClick = this.handleSignUpClick.bind(this);
	  this.goBack = this.goBack.bind(this);

    }

    handleLoginClick(){
      this.setState({display: 'login'});
    }

    handleSignUpClick(){
      this.setState({display: 'sign-up'});
    }
	
	goBack(){
		this.setState({display: 'welcome'});
	}

render() {
  let element;
        if (this.state.display === 'welcome'){
          element = (
            <div>
              <img src={logo} className="welcomeLogo"/><br />
              <button onClick={this.handleLoginClick} className="login">Login</button>
			  <br />
              <button onClick={this.handleSignUpClick} className="sign-up">Sign Up</button>
            </div>
          );
        } else if (this.state.display === 'login'){
          element = <Login screenDisplay={this.props.screenDisplay} loginHandler={this.props.loginHandler} goBack={this.goBack}/>;
        } else if (this.state.display === 'sign-up') {
          element = <SignUp goBack={this.goBack} signUpHandler={this.props.signUpHandler}/>;
        }
  return (
    <div>
      {element}
    </div>
  )
}
}

export default Start;
