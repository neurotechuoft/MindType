from socketIO_client import SocketIO
import random
import time

def on_retrieve_prediction_results(*args):
    print(args)
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

def print_results(*args):
    print(args)

# p300 server running on localhost:8001
socket_client = SocketIO('localhost', 8002)
socket_client.connect()

uuid = random.randint(0, 1e10)
timestamp = 85725
p300 = 1
user = "karl"
password = "cui"
email = "e@mail"

socket_client.emit("predict", (uuid, timestamp), on_retrieve_prediction_results)
socket_client.wait_for_callbacks(seconds=1)

# socket_client.emit("login", (user, password), print_results)
# socket_client.wait_for_callbacks(seconds=1)

# for i in range(30):
#     if i % 10 == 0:
#         print("iter", i)
#
#     uuid = random.randint(0, 1e10)
#     p300 = random.choice([0, 1])
#     socket_client.emit("train", (uuid, timestamp + i*.5, p300), print_results)
#     socket_client.wait_for_callbacks(seconds=.5)
#
#     time.sleep(.5)

# socket_client.emit("register", (user, password, email), print_results)
# socket_client.wait_for_callbacks(seconds=1)

# socket_client.emit("logout", None, print_results)
# socket_client.wait_for_callbacks(seconds=1)
