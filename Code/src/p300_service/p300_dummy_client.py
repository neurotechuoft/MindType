from socketIO_client import SocketIO

class P300Client(object):

    def __init__(self):
        results = []
        socket_client = None

    def on_retrieve_prediction_results(self, *args):
        def on_retrieve_results(sid=args[0], results=args[1]):
            uid, ts, p300 = results
            print(f'p300: {p300}')
        return on_retrieve_results()

    def connect(self, ip, port):
        self.socket_client = SocketIO(ip, port)
        self.socket_client.connect()

    def predict(self, user_id, timestamp, eeg_data):
        data = (user_id, timestamp, eeg_data)
        self.socket_client.emit("retrieve_prediction_results", data, self.on_retrieve_prediction_results)
        self.socket_client.wait_for_callbacks(seconds=1)


if __name__ == '__main__':
    p300_client = P300Client()
    p300_client.connect("localhost", 8001)

    user_id = 1123
    timestamp = 1238794
    eeg_data = ['data']
    p300_client.predict(user_id, timestamp, eeg_data)
