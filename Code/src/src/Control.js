import React, { Component } from 'react';
import App from './containers/App';
import Start from './Start';
import Intro from './Intro';
import InstructionOneLetter from './InstructionOneLetter';
import InstructionOneWord from './InstructionOneWord';
import LetterSwitch from './LetterSwitch';
import EmojiSwitch from './EmojiSwitch';
import NumberSwitch from './NumberSwitch';
import WordMind from './WordMind';
import Sentence from './Sentence';
import SentenceEmoji from './SentenceEmoji';
import PredictivePractice from './PredictivePractice';
import Final from './Final';

class Control extends React.Component {
  constructor(props) {
      super(props);
      this.state = {screenDisplay: 'start'};
	  this.loginHandler = this.loginHandler.bind(this);
	  this.signUpHandler = this.signUpHandler.bind(this);
	  this.introHandler = this.introHandler.bind(this);
	  this.instructionOneLetterHandler = this.instructionOneLetterHandler.bind(this);
	  this.instructionOneWordHandler = this.instructionOneWordHandler.bind(this);
	  this.letterSwitchHandler = this.letterSwitchHandler.bind(this);
	  this.emojiSwitchHandler = this.emojiSwitchHandler.bind(this);
	  this.numberSwitchHandler = this.numberSwitchHandler.bind(this);
	  this.wordMindHandler = this.wordMindHandler.bind(this);
	  this.sentenceHandler = this.sentenceHandler.bind(this);
	  this.sentenceEmojiHandler = this.sentenceEmojiHandler.bind(this);
	  this.predictiveHandler = this.predictiveHandler.bind(this);
	  this.finalHandler = this.finalHandler.bind(this);
    }
	
	loginHandler(){
		this.setState({screenDisplay: 'app'});
	}
	
	signUpHandler(){
		this.setState({screenDisplay: 'intro'});
	}
	
	introHandler(){
		this.setState({screenDisplay: 'instructionOneLetter'});
	}
	
	instructionOneLetterHandler(){
		this.setState({screenDisplay: 'instructionOneWord'});
	}
	
	instructionOneWordHandler(){
		this.setState({screenDisplay: 'letterSwitch'});
	}
	
	letterSwitchHandler(){
		this.setState({screenDisplay: 'emojiSwitch'});
	}
	
	emojiSwitchHandler(){
		this.setState({screenDisplay: 'numberSwitch'});
	}
	
	numberSwitchHandler(){
		this.setState({screenDisplay: 'wordMind'});
	}
	
	wordMindHandler(){
		this.setState({screenDisplay: 'sentence'});
	}
	
	sentenceHandler(){
		this.setState({screenDisplay: 'sentenceEmoji'});
	}
	
	sentenceEmojiHandler(){
		this.setState({screenDisplay: 'predictivePractice'});
	}
	
	predictiveHandler(){
		this.setState({screenDisplay: 'final'});
	}
	
	finalHandler(){
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
		} else if (this.state.screenDisplay === 'instructionOneLetter'){
		  element = <InstructionOneLetter instructionOneLetterHandler={this.instructionOneLetterHandler}/>;
		} else if (this.state.screenDisplay === 'instructionOneWord'){
		  element = <InstructionOneWord instructionOneWordHandler={this.instructionOneWordHandler}/>;
		} else if (this.state.screenDisplay === 'letterSwitch'){
		  element = <LetterSwitch letterSwitchHandler={this.letterSwitchHandler} />;
		} else if (this.state.screenDisplay === 'emojiSwitch'){
		  element = <EmojiSwitch emojiSwitchHandler={this.emojiSwitchHandler} />;
		} else if (this.state.screenDisplay === 'numberSwitch'){
		  element = <NumberSwitch numberSwitchHandler={this.numberSwitchHandler} />;
		} else if (this.state.screenDisplay === 'wordMind'){
		  element = <WordMind wordMindHandler={this.wordMindHandler} />
		} else if (this.state.screenDisplay === 'sentence'){
		  element = <Sentence sentenceHandler={this.sentenceHandler} />
		} else if (this.state.screenDisplay === 'sentenceEmoji'){
		  element = <SentenceEmoji sentenceEmojiHandler={this.sentenceEmojiHandler} />
		} else if (this.state.screenDisplay === 'predictivePractice'){
		  element = <PredictivePractice predictiveHandler={this.predictiveHandler} />
		} else if (this.state.screenDisplay === 'final'){
		  element = <Final finalHandler={this.finalHandler} />
		}
  return (
    <div>
      {element}
    </div>
  )
}
}

export default Control;
