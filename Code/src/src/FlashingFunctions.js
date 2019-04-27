export function resetKey(key) {
	if (key != null) {
	  key.classList.add("entry");
	  key.classList.remove("selected");
	  key.classList.remove("chosen");
	}
}

export function keyChosen(key) {
	if (key != null) {
	  key.classList.add("chosen");
	}
}

export function writePhrase() {
	const {statement, interval, lettersFound, rowOrder, 
	  colOrder, rowFound, colFound, displayText} = this.state;
	if (lettersFound === statement.length) {
	  clearInterval(interval);
	} else {
	  for (let j = 0; j < prev.length; j++) {
		this.resetKey(prev[j]);
	  }
	  if (selectedKey != null) {
		this.resetKey(selectedKey);
	  }
	  
	  // making sure rows/cols don't flash if they've already been found.
	  let rc;
	  if (rowFound) rc = 2;
	  else if (colFound) rc = 1;
	  else rc = Math.floor((Math.random() * 2) + 1);
	  
	  if (rc === 1) {
		const row = rows[rowOrder[curRow]];
		prev = row;
		curRow = curRow + 1;

		// Handling Spaces 

		if (statement[lettersFound] === ' ' && row === rows[4]) {
		  const rowOrder = getRandomArray(5);
		  curRow = 0;
		  this.setState({rowFound : true, rowOrder});
		}
		for (let j = 0; j < row.length; j++) {
		  row[j].classList.remove("entry");
		  row[j].classList.add("selected");
		  if (row[j].innerHTML === statement[lettersFound]) {
			if (colFound) {
			  selectedKey = row[j];
			  // row[j].classList.add("chosen");
			}
			// numColumSelected = j;
			const rowOrder = getRandomArray(5);
			curRow = 0;
			this.setState({rowFound : true, rowOrder});
		  }
		}
	  } else {
		const col = cols[colOrder[curCol]];
		prev = col;
		curCol = curCol + 1;
		
		// Handling Spaces
		if (statement[lettersFound] === ' ' && col === cols[0]) {
		  const colOrder = getRandomArray(6);
		  curCol = 0;
		  this.setState({colFound : true, colOrder});
		}

		for (let j = 0; j < col.length; j++) {
		  col[j].classList.remove("entry");
		  col[j].classList.add("selected");
		  if (col[j].innerHTML === statement[lettersFound]) {
			if (rowFound) {
			  selectedKey = col[j];
			  // col[j].classList.add("chosen");
			}
			const colOrder = getRandomArray(6);
			curCol = 0;
			this.setState({colFound : true, colOrder});
		  }
		}
	  }
	  // If a letter has been found.
	  if (rowFound && colFound) {
		this.keyChosen(selectedKey);
		// TODO: Reset numCol and numRow to -1
		[curRow, curCol] = [0, 0];
		const newDisplay = displayText + statement[lettersFound];
		this.setState({rowFound : false, colFound : false, 
		displayText : newDisplay, lettersFound : lettersFound + 1});
		// Emitting an event to the socket to type letter.
		robot_socket.emit('typing', statement[lettersFound]);
		// Emitting an event to the socket to recieve word predictions.
		nlp_socket.emit("autocomplete", newDisplay, this.handlePredictions);
	  }
	}
}

export default FlashingFunctions