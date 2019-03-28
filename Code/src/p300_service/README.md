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
