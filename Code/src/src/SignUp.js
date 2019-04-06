import React, { Component } from 'react';

class SignUp extends React.Component {
  render(){
    return (
      <div>
        <img src="mindTypeLogo.png"className="logo"/><br />
        <br/>
        <input type="text" className="name-user" placeholder="Name"></input><br />
        <br />
        <input type="email" className="email-input" placeholder="Email"></input><br />
        <br />
        <input type="password" className="password-input" placeholder="Password"></input><br />
        <br />
        <button className="sign-up" onClick={this.props.signUpHandler}>Sign Up</button>
		<button className="back" onClick={this.props.goBack}>Go Back</button>
      </div>
    )
  }
}

export default SignUp;
