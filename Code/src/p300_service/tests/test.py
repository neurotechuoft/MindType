from socketIO_client import SocketIO
import random

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

uuid = random.randint(0, 1e10)
timestamp = random.randint(0, 1e7)
p300 = 1

socket_client.emit("predict", (uuid, timestamp), on_retrieve_prediction_results)
socket_client.wait_for_callbacks(seconds=1)

socket_client.emit("train", (uuid, timestamp, p300), on_train_results)
socket_client.wait_for_callbacks(seconds=1)
