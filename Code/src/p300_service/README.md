## P300 Service

There are 2 main components: the P300 Client and the P300 Server. The client is responsible for communicating with and coordinating between the front end (via SocketIO), the muse headband (through an LSL stream), and the server (again with SocketIO). The server stores user data and does ML training and predictions.

#### P300 Server Usage

The server:
- has a PostGres database where it stores username and password info
- saves classifiers after training
- returns accuracy scores to the P300 client incrementally during training
- returns predictions to the P300 client

To start the server, run `python p300_server.py`.

#### P300 Client Usage

To start the client, first start a muselsl stream (with [BlueMuse](https://github.com/kowalej/BlueMuse)). Run `python p300_client.py` to start the client. This will connect to the muselsl stream and the server (so you need the server running beforehand).

Client API:
###### Predict
- With SocketIO, `emit("predict", (uuid, timestamp), callback_function)`
- Returns `sid, (uuid, p300, score)`, where score is the confidence in the prediction, and p300 is True or False depending on whether the classifier thinks there's a p300.

###### Train
- With SocketIO, `emit("train", (uuid, timestamp, p300), callback_function)` where p300 is either 0 or 1 (boolean).
- Returns `sid, accuracy`, where accuracy is the current accuracy of the classifier, or None/null if there isn't enough data.

###### Log in
- With SocketIO, `emit("login", (username, password), callback_function)`
- Returns `sid, success`, where success is either True or False.

###### Log out
- With SocketIO, `emit("logout", None, callback_function)`
- Returns `sid, success`, where success is either True or False.

###### Register
- With SocketIO, `emit("register", (username, password, email), callback_function)`
- Returns `sid, success`, where success is either True or False.

## Testing with the dummy server
Run `python p300_dummy_client.py` to start the dummy client. From there, for example to log in, run:

```
from socketIO_client import SocketIO

def print_results(*args):
    print(args)

user = "username"
password = "password"

# p300 client running on localhost:8001
socket_client = SocketIO('localhost', 8001)
socket_client.connect()

socket_client.emit("login", (user, password), print_results)
socket_client.wait_for_callbacks(seconds=1)
```

And this prints `('9780af84c6c84a7289c5bab1f8fe9adf', False)`.

## Helpful Links

[microsoft powershell policies](https://docs.microsoft.com/en-gb/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-6&viewFallbackFrom=powershell-Microsoft.PowerShell.Core)

[python windows](https://www.python.org/downloads/windows/)

[virtualenv windows](http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/)

[bluemuse](https://github.com/kowalej/BlueMuse)

[muselsl](https://github.com/alexandrebarachant/muse-lsl)

[p300 notebook](https://github.com/NeuroTechX/eeg-notebooks/blob/master/notebooks/P300.ipynb)

[mne raw files](https://martinos.org/mne/dev/auto_examples/io/plot_read_and_write_raw_data.html)

[socketio](https://python-socketio.readthedocs.io/en/latest/)

## P300 Service Notes
- What parameters do we want to custom define?
    - filter frequencies
    - trial number per epoch
    - marker identities (letters)
    - input data format
    - return data format

How is data inputted into P300 service:
- create lsl stream object and create server messages
- create

How should data be returned:
- dfdf



## Dummy client usage

Start the p300 dummy client with `python p300_dummy_client.py`. This creates a dummy client and initializes handlers for requests.

Connect to this dummy with a SocketIO client, and emit `predict` to make a prediction and `train` to train the classifier with p300 data. Example from `tests/test.py`:
```
from socketIO_client import SocketIO
import random


# callback functions to print out results
def on_retrieve_prediction_results(*args):
    sid = args[0]
    results = args[1]
    uuid, p300, score = results
    print(f'p300: {p300}')
    print(f'score: {score}')

def on_train_results(*args):
    sid = args[0]
    results = args[1]
    uuid, accuracy = results
    print(f'accuracy: {accuracy}')


# p300 server running on localhost:8001
socket_client = SocketIO('localhost', 8001)
socket_client.connect()

# generate random values for parameters (for testing)
uuid = random.randint(0, 1e10)
timestamp = random.randint(0, 1e7)
p300 = 1

# predict whether p300 happens
socket_client.emit("predict", (uuid, timestamp), on_retrieve_prediction_results)
socket_client.wait_for_callbacks(seconds=1)

# train with a timestamp and p300 target
socket_client.emit("train", (uuid, timestamp, p300), on_train_results)
socket_client.wait_for_callbacks(seconds=1)
```
