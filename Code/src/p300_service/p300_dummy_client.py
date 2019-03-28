from socketIO_client import SocketIO


# callback functions to print results
def on_retrieve_prediction_results(*args):
    sid=args[0]
    results=args[1]
    uuid, p300, score = results
    print(f'p300: {p300}')
    print(f'score: {score}')

def on_train_results(*args):
    sid=args[0]
    results=args[1]
    uuid, acc = results
    print(f'accuracy: {acc}')


class P300Client(object):

    def __init__(self):
        self.results = []
        self.socket_client = None
        self.streams = {}

    def connect(self, ip, port):
        self.socket_client = SocketIO(ip, port)
        self.socket_client.connect()

    def disconnect(self):
        self.socket_client.disconnect()

    # for testing
    def predict(self, uuid, timestamp, callback_func=on_retrieve_prediction_results):
        data = (uuid, timestamp)
        self.socket_client.emit("retrieve_prediction_results_test", data, callback_func)
        self.socket_client.wait_for_callbacks(seconds=1)

    def train(self, uuid, timestamp, p300, callback_func=on_train_results):
        data = (uuid, timestamp, p300)
        self.socket_client.emit("train_classifier_test", data, callback_func)
        self.socket_client.wait_for_callbacks(seconds=1)



if __name__ == '__main__':
    p300_client = P300Client()
    p300_client.connect("localhost", 8001)

    user_id = 1123
    timestamp = 53423
    p300 = True

    p300_client.train(user_id, timestamp, p300)
    p300_client.predict(user_id, timestamp)

    p300_client.disconnect()
