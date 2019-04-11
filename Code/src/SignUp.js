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
        <button className="sign-up">Sign Up</button>
      </div>
    )
  }
}

export default SignUp;
