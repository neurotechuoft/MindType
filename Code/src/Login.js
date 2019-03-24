import React, { Component } from 'react';

class Login extends React.Component {
  render(){
    return (
      <div>
        <img src="mindTypeLogo.png" className="logo"/><br />
        <br/>
        <input type="email" className="email-input" placeholder="Email"></input><br />
        <br />
        <input type="password" className="password-input" placeholder="Password"></input><br />
        <br />
        <button className="login">Login</button>
      </div>
    )
  }
}

export default Login;
