import React, { Component } from 'react';
import logo from './mindtype_logo.png';
import io from "socket.io-client";

const nlp_socket = io('http://34.73.165.89:8001'); // Socket to connect to NLP Service.
const robot_socket = io('http://localhost:8002'); // Socket to connect to RobotJS

class SignUp extends React.Component {
	
	constructor(props) {
    super(props);
	this.state = { 
      emailValue: '',
	  passwordValue: '',
	  nameValue: ''
    };
    this.handleSignUpClick = this.handleSignUpClick.bind(this);
	this.checkSignUp = this.checkSignUp.bind(this);
  }
	
  handleSignUpClick(){
	 //robot_socket.emit("register", (this,state.nameValue, this.state.emailValue, this.state.passwordValue, this.state.nameValue), this.checkSignUp);
	 this.props.signUpHandler();
  }
  
  checkSignUp(sid, tf){
	  if (tf === false){
		alert('The information you entered is invalid or the email is already taken');
	  } else {
		  this.props.signUpHandler();
	  }
  }
  
  render(){
    return (
      <div>
        <img src={logo} className="logoMindType"/><br />
        <br/>
        <input type="text" className="name-user" placeholder="Name" value={this.nameValue}></input><br />
        <br />
        <input type="email" className="email-input" placeholder="Email" value={this.emailValue}></input><br />
        <br />
        <input type="password" className="password-input" placeholder="Password" value={this.passwordValue}></input><br />
        <br />
        <button className="sign-up" onClick={this.handleSignUpClick}>Sign Up</button>
		<br />
		<button className="back" onClick={this.props.goBack}>Go Back</button>
      </div>
    )
  }
}

export default SignUp;
