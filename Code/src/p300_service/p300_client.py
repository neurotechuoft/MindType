import time

from socketIO_client import SocketIO
from sanic import Sanic
from eeg_stream import EEGStream
from marker_stream import MarkerStream
from ml_stream import MLStream

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

    def on_retrieve_prediction_results(self, *args):
        def on_retrieve_results(sid=args[0], results=args[1]):
            uid, ts, p300 = results
            print(f'p300: {p300}')
        return on_retrieve_results()

    def create_streams(self):
        self.streams['eeg'] = self._create_eeg_stream()
        self.streams['marker'] = self._create_marker_stream()

        # TODO: data is only variable between training (ie. first time the app
        # is opened) and predictions. The contents of data need to be synced
        # with the front end and database, based on what the user wants.
        data = {'classifier_path': 'tests/data/classifier.pkl',
                'test_path': 'tests/data/test_data.pickle',
                'event_time': 0.4,      # or 0.2?
                'train': False,
                'train_epochs': 120,    # 120 for 2 min, 240 for 4 min
                'get_test': False}

        self.streams['ml'] = self._create_ml_stream(data)

    def start_streams(self):
        for stream in ['eeg', 'marker', 'ml']:
            self._start_stream(stream)

    def train_classifier(self, user_id):
        inputs, targets = self.streams['ml'].get_training_data()
        if inputs is None or targets is None:
            raise Exception("No data to use for training")
        else:
            eeg_data = (inputs, targets)
            data = (user_id, timestamp, eeg_data)
            self.socket_client.emit("train_classifier", data, None)
            self.socket_client.wait_for_callbacks(seconds=1)

    def predict(self, user_id):
        eeg_data = self.streams['ml'].get_prediction_data()
        if eeg_data is None:
            raise Exception("No data to make predictions for")
        else:
            eeg_data.get('prediction_data')
            data = (user_id, eeg_data)
            self.socket_client.emit("retrieve_prediction_results", data, self.on_retrieve_prediction_results)
            self.socket_client.wait_for_callbacks(seconds=1)


    #
    # Private methods for creating and starting streams
    #

    def _create_eeg_stream(self):
        return EEGStream(thread_name='EEG_data', event_channel_name='P300')

    def _create_marker_stream(self):
        return MarkerStream()

    def _create_ml_stream(self, data):
        if self.streams.get('eeg') is None:
            raise Exception(f"EEG stream does not exist")
        if self.streams.get('marker') is None:
            raise Exception(f"Marker stream does not exist")

        return MLStream(m_stream=self.streams['marker'],
                        eeg_stream=self.streams['eeg'],
                        classifier_path=data['classifier_path'],
                        test_path=data['test_path'],
                        event_time=data['event_time'],
                        train=data['train'],
                        train_epochs=data['train_epochs'],
                        get_test=data['get_test'])

    def _start_stream(self, stream):
        if self.streams.get(stream) is None:
            raise RuntimeError("Cannot start {0} stream, stream does not exist".format(stream))
        else:
            if stream == 'ml':
                while not (self.streams['eeg'].data and self.streams['marker'].data):
                    time.sleep(0.1)
                self.streams[stream].start()
            else:
                self.streams[stream].lsl_connect()


if __name__ == '__main__':
    p300_client = P300Client()
    p300_client.create_streams()
    p300_client.start_streams()
    p300_client.connect("localhost", 8001)

    p300_client.disconnect()
