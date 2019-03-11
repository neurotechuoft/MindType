import React, { Component } from 'react';
import SignUp from 'SignUp';
import Login from 'Login';

class Start extends React.Component {
  constructor(props) {
      super(props);
      this.state = {display: 'welcome'};
      this.handleLoginClick = this.handleLoginClick.bind(this);
      this.handleSignUpClick = this.handleSignUpClick.bind(this);
    }

    handleLoginClick(){
      this.setState({display: 'login'});
    }

    handleSignUpClick(){
      this.setState({display: 'sign-up'});
    }

render() {
  let element;
        if (this.state.display === 'welcome'){
          element = (
            <div>
              <img src="mindTypeWelcome.png" className="welcomeLogo"/><br />
              <button onClick={this.handleLoginClick} className="login">Login</button>
              <br /><br />
              <button onClick={this.handleSignUpClick} className="sign-up">Sign Up</button>
            </div>
          );
        } else if (this.state.display === 'login'){
          element = <Login />;
        } else if (this.state.display === 'sign-up') {
          element = <SignUp />;
        }
  return (
    <div>
      {element}
    </div>
  )
}
}

export default Start;
