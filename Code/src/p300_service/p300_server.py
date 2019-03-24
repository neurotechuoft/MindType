from sanic import Sanic
import socketio
from eeg_stream import EEGStream
from marker_stream import MarkerStream
from ml_stream import MLStream
import ml

# for testing
import random


class P300Service:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)

        self.clfs = {}

    async def train_classifier(self, sid, args):
        uid, ts, data = args
        i, t = data
        self.clfs[sid] = ml.ml_classifier(i, t, pipeline='vect_lr')

    async def retrieve_prediction_results(self, sid, args):
        if self.clfs[sid] is None:
            raise Exception("Cannot start ML stream with sid {}".format(sid))
        else:
            uid, ts, data = args
            p300 = self.clfs[sid].predict(data)
            results = (uid, ts, p300)
            return sid, results

    # for testing
    async def retrieve_prediction_results_test(self, sid, args):
        uid, ts, data = args
        p300 = random.choice([True, False])
        results = (uid, ts, p300)
        return sid, results


    def initialize_handlers(self):
        self.sio.on("retrieve_prediction_results", self.retrieve_prediction_results_test)
        self.sio.on("train_classifier", self.train_classifier)


if __name__ == '__main__':
    service = P300Service()
    service.initialize_handlers()
    service.app.run(host='localhost', port=8001)
