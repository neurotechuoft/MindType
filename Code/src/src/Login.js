import React, { Component } from 'react';
import logo from './mindTypeLogo.png';

class Login extends React.Component {
	

	
  render(){
    return (
      <div>
        <img src={logo} className="logoMindType"/><br />
        <br/>
        <input type="email" className="email-input" placeholder="Email"></input><br />
        <br />
        <input type="password" className="password-input" placeholder="Password"></input><br />
        <br />
        <button className="login" onClick={this.props.loginHandler}>Login</button>
		<br />
		<button className="back" onClick={this.props.goBack}>Go Back</button>
      </div>
    )
  }
}

export default Login;
