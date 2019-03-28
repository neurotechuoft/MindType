from socketIO_client import SocketIO
import random

def on_retrieve_prediction_results(results):
    uuid, p300, score = results
    print(f'p300: {p300}')
    print(f'score: {score}')

# p300 server running on localhost:8002
socket_client = SocketIO('localhost', 8002)
socket_client.connect()

uuid = random.randint(0, 2**20)
timestamp = random.randint(0, 80000)
p300 = 1

socket_client.emit("predict", (uuid, timestamp), on_retrieve_prediction_results)
socket_client.wait_for_callbacks(seconds=1)
