from sanic import Sanic
import socketio

from eeg_stream import EEGStream
from marker_stream import MarkerStream
from ml_stream import MLStream
import ml

import numpy as np

# for testing
import random


class P300Service:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)

        self.clfs = {}

    async def train_classifier(self, sid, args):
        uid, data = args
        i, t = data
        i = np.array(i)
        t = np.array(t)

        # Note in Barachant's ipynb, 'erpcov_mdm' performed best. 'vect_lr' is the
        # universal one for EEG data.
        self.clfs[uid] = ml.ml_classifier(i, t, pipeline='vect_lr')
        ml.save(f"clf/{uid}.pkl", classifier)

    async def load_classifier(self, sid, uid):
        try:
            self.clfs[uid] = ml.load(f"clf/{uid}.pkl")
        except FileNotFoundError:
            raise Exception(f"There is no trained classifier with user id {uid}")

    async def retrieve_prediction_results(self, sid, args):
        uid, data = args
        if self.clfs[uid] is None:
            raise Exception(f"Cannot start ML stream with user id {uid}")
        else:
            uid, data = args
            p300 = self.clfs[sid].predict(data)
            results = (uid, p300)
            return sid, results

    # for testing
    async def retrieve_prediction_results_test(self, sid, args):
        uid, data = args
        p300 = random.choice([True, False])
        results = (uid, p300)
        return sid, results


    def initialize_handlers(self):
        self.sio.on("retrieve_prediction_results", self.retrieve_prediction_results_test)
        self.sio.on("train_classifier", self.train_classifier)
        self.sio.on("load_classifier", self.load_classifier)



if __name__ == '__main__':
    service = P300Service()
    service.initialize_handlers()
    service.app.run(host='localhost', port=8001)
