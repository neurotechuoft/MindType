import React, { Component } from 'react';

class Intro extends React.Component {
	
	
  render(){
    return (
      <div className="explanation">
        <center><img src="mindTypeLogo.png" />
    <h1>What is MindType?</h1></center>
    <h3>MindType is a mind-controlled keyboard that lets you type letters, words, numbers and characters using your brain
activity! </h3>

    <center><h1>How Does It Work?</h1></center>

    <h3>Let's start with a thought experiment.</h3>

    <h3>Imagine you have a bag of balls, which are all <span className="blueText">blue</span> except for one <span className="redText">red</span> ball.</h3>

    <h3><span className="redText">You want the red ball.</span></h3>
<center>
    <img src="redball.png" height="200" width="200" />

    <img src="dice.png" height="200" width="222"/>
</center>
    <h3>Now suppose I start randomly removing the balls. One by one, you see blue ball after blue ball removed from the bag until suddenly, after patiently waiting, you see the red ball emerge.</h3>

    <h3>Because you knew what you were looking for but you didn't know when you'll see it exactly, the moment you saw the red ball finally removed, it triggered a neurological reaction
detectable by measuring your brain activity.</h3>

  <h3>This is known as the P300 oddball paradigm and it's the foundation for the keyboard's functionality.</h3>

<h3>The keyboard relies on the P300 mechanism by randomly flashing rows and columns of letters, symbols and numbers.
When you see a row with the letter you want, but you don't know when it's going to happen exactly, it triggers the
P300 reaction in your brain - and the same happens when a row with the letter is randomly flashed. Your EEG headset
detects the specific change in your brain's electrical activity associated with the P300. When both a row and a column with a particular item of interest (such as the letter 'p') triggers this response, our code will type the
letter on the screen.

      </h3>

      <center><img src="simpsonMind.jpg" /></center>

<h3> Now you know how it works. Let's practice using the keyboard!</h3>
<button className="continueButton" onClick={this.props.introHandler}>Continue</button>
      </div>
    )
  }
}

export default Intro;