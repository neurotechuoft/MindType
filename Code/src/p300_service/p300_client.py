import pylsl
import socketio
from socketIO_client import SocketIO
from sanic import Sanic
import threading
import time

from eeg_stream import EEGStream
from marker_stream import MarkerStream
from ml_stream import MLStream

from tests.test_marker_publisher import test_marker_stream, start_marker_stream


class P300Client(object):

    def __init__(self):
        self.socket_client = None
        self.marker_outlet = None
        self.train_mode = True  # True for training mode, False for prediction mode
                                # will stay in training mode until first prediction
        self.train_results = []
        self.pred_results = []
        self.streams = {}

        self.register_results = None
        self.login_results = None
        self.logout_results = None

        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)

    def connect(self, ip, port):
        self.socket_client = SocketIO(ip, port)
        self.socket_client.connect()

    def disconnect(self):
        self.socket_client.disconnect()

    def create_streams(self):
        self.streams['eeg'] = self._create_eeg_stream()
        self.streams['marker'] = self._create_marker_stream()

        # TODO: some kind of switching between training and prediction modes
        data = {'event_time': 0.4,      # or 0.2?
                'train_epochs': 120}    # 120 for 2 min, 240 for 4 min

        self.streams['ml'] = self._create_ml_stream(data)

    def start_streams(self):
        for stream in ['eeg', 'marker', 'ml']:
            self._start_stream(stream)

    def change_mode(self, train_mode=False):
        """ train_mode=True for training mode
            train_mode=False for prediction mode """
        if self.streams['ml'] is None:
            raise Exception(f"ml stream does is not running")

        curr_mode = self.streams['ml'].get_mode()
        if curr_mode is not train_mode:
            self.train_mode = train_mode
            self.streams['ml'].set_mode(train_mode)

    async def start_event_loop(self):
        """Continuously pulls data from ml_stream and sends to server based on
        whether we are training or predicting"""
        if self.streams.get('ml') is None:
            raise Exception(f"ml stream does not exist")

        data = None
        while data is None:
            # send training jobs to server
            if self.train_mode:
                data = self.streams['ml'].get_training_data()
                if data is not None:
                    uuid = data['uuid']
                    train_data = data['train_data']
                    train_targets = data['train_targets']
                    self.train(uuid, train_data, train_targets)
                    return

            # send prediction jobs to server
            else:
                data = self.streams['ml'].get_prediction_data()
                if data is not None:
                    uuid = data['uuid']
                    eeg_data = data['eeg_data']
                    self.predict(uuid, eeg_data)
                    return

            time.sleep(0.1)

    #
    # Callback funcs
    #

    def on_retrieve_prediction_results(self, *args):
        results=args[1]
        self.pred_results.append(results)

    def on_train_results(self, *args):
        results=args[1]
        self.train_results.append(results)

    def on_register_results(self, *args):
        self.register_results = args

    def on_login_results(self, *args):
        self.login_results = args

    def on_logout_results(self, *args):
        self.logout_results = args

    #
    # Server-side communication
    #

    def predict(self, uuid, eeg_data):
        data = (uuid, eeg_data)
        self.socket_client.emit("retrieve_prediction_results", data, self.on_retrieve_prediction_results)
        self.socket_client.wait_for_callbacks(seconds=1)

    def train(self, uuid, eeg_data, p300):
        data = (uuid, eeg_data, p300)
        self.socket_client.emit("train_classifier", data, self.on_train_results)
        self.socket_client.wait_for_callbacks(seconds=1)

    def register(self, username, password, email):
        data = (username, password, email)
        self.socket_client.emit("register", data, self.on_register_results)
        self.socket_client.wait_for_callbacks(seconds=1)
        while not self.register_results:
            time.sleep(.1)
        return self.register_results

    def login(self, username, password):
        data = (username, password)
        self.socket_client.emit("login", data, self.on_login_results)
        self.socket_client.wait_for_callbacks(seconds=1)
        while not self.login_results:
            time.sleep(.1)
        return self.login_results

    def logout(self):
        self.socket_client.emit("logout", None, self.on_logout_results)
        self.socket_client.wait_for_callbacks(seconds=1)
        while not self.logout_results:
            time.sleep(.1)
        return self.logout_results

    #
    # Private methods for creating and starting streams
    #

    @staticmethod
    def _create_eeg_stream():
        return EEGStream(thread_name='EEG_data', event_channel_name='P300')

    def _create_marker_stream(self):
        info = pylsl.StreamInfo('Markers', 'Markers', 4, 0, 'string', 'mywid32')
        self.marker_outlet = pylsl.StreamOutlet(info)

        return MarkerStream(thread_name='Marker_stream')

    def _create_ml_stream(self, data):
        if self.streams.get('eeg') is None:
            raise Exception(f"EEG stream does not exist")
        if self.streams.get('marker') is None:
            raise Exception(f"Marker stream does not exist")

        return MLStream(m_stream=self.streams['marker'],
                        eeg_stream=self.streams['eeg'],
                        event_time=data['event_time'],
                        train_epochs=data['train_epochs'])

    def _start_stream(self, stream):
        if self.streams.get(stream) is None:
            raise RuntimeError("Cannot start {0} stream, stream does not exist".format(stream))
        elif stream == 'ml':
            self.streams[stream].start(self.train_mode)
        else:
            self.streams[stream].lsl_connect()

    #
    # Handlers for communication with front end
    #

    def initialize_handlers(self):
        self.sio.on("train", self.train_handler)
        self.sio.on("predict", self.predict_handler)

        self.sio.on("register", self.register_handler)
        self.sio.on("login", self.login_handler)
        self.sio.on("logout", self.logout_handler)

    async def register_handler(self, sid, args):
        username, password, email = args
        return self.register(username, password, email)

    async def login_handler(self, sid, args):
        username, password = args
        return self.login(username, password)

    async def logout_handler(self, sid, args):
        return self.logout()

    async def train_handler(self, sid, args):
        if not self.train_mode:
            self.change_mode(train_mode=True)
            time.sleep(.2)

        uuid, timestamp, p300 = args
        package = [
            str(timestamp),
            str(p300),      # target
            str(1),         # 1 event total
            str(uuid)       # take uuid for epoch id
        ]
        self.marker_outlet.push_sample(package)
        await self.start_event_loop()

        while len(self.train_results) == 0:
            time.sleep(.1)
        score = self.train_results.pop(0)
        return sid, score

    async def predict_handler(self, sid, args):
        if self.train_mode:
            self.change_mode(train_mode=False)
            time.sleep(.2)

        uuid, timestamp = args
        package = [
            str(timestamp),
            str(0),         # target
            str(1),         # 1 event total
            str(uuid)       # take uuid for epoch id
        ]
        self.marker_outlet.push_sample(package)
        await self.start_event_loop()

        while len(self.pred_results) == 0:
            time.sleep(.1)
        pred = self.pred_results.pop(0)
        return sid, pred



if __name__ == '__main__':

    p300_client = P300Client()
    p300_client.create_streams()
    p300_client.start_streams()

    # connect to p300 server
    # p300_client.connect('35.222.93.233', 8001)
    p300_client.connect('localhost', 8001)

    # run client as server as well (to allow API for front end)
    p300_client.initialize_handlers()
    p300_client.app.run(host='localhost', port=8002)
