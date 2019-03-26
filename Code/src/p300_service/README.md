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

Start P300 server:
```
from p300_server import P300Service

service = P300Service()
service.initialize_handlers()
service.app.run(host='localhost', port=8001)
```

Start P300 client, try making a prediction and sending some training data:
```
from p300_dummy_client import P300Client

p300_client = P300Client()
p300_client.connect("localhost", 8001)

user_id = 1123
timestamp = 53423
p300 = True

p300_client.train(user_id, timestamp, p300)
p300_client.predict(user_id, timestamp)
```

The prints for accuracy, p300, and score are the default callback functions (in p300_dummy_client.py). You may optionally pass in a callback function as another parameter to train and predict. For example:
```
def on_retrieve_prediction_results(*args):
    sid=args[0]
    results=args[1]
    uuid, p300, score = results
    print(f'p300: {p300}')
    print(f'score: {score}')
    
p300_client.predict(user_id, timestamp, on_retrieve_prediction_results)
```
