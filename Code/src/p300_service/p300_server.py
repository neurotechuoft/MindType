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

        self.clf = None

    async def load_classifier(self, sid):
        try:
            self.clf = ml.load(f"tests/data/classifier.pkl")
        except FileNotFoundError:
            raise Exception(f"Cannot load classifier")

    async def train_classifier(self, sid, args):
        uuid, eeg_data, p300 = args
        i = np.array(eeg_data)
        t = np.array(p300)

        # Note in Barachant's ipynb, 'erpcov_mdm' performed best. 'vect_lr' is the
        # universal one for EEG data.
        self.clf = ml.ml_classifier(i, t, pipeline='vect_lr')
        ml.save(f"tests/data/clf.pkl", classifier)

    async def retrieve_prediction_results(self, sid, args):
        uuid, data = args
        p300 = self.clf.predict(data)
        results = (uid, p300)
        return sid, results


    # for testing
    async def retrieve_prediction_results_test(self, sid, args):
        uuid, eeg_data = args
        p300 = random.choice([True, False])
        score = random.random()
        results = (uuid, p300, score)
        return sid, results

    async def train_classifier_test(self, sid, args):
        uuid, eeg_data, p300 = args
        acc = random.random()
        results = (uuid, acc)
        return sid, results


    def initialize_handlers(self):
        self.sio.on("retrieve_prediction_results", self.retrieve_prediction_results)
        self.sio.on("train_classifier", self.train_classifier)
        self.sio.on("load_classifier", self.load_classifier)

        # for testing
        self.sio.on("retrieve_prediction_results_test", self.retrieve_prediction_results_test)
        self.sio.on("train_classifier_test", self.train_classifier_test)


if __name__ == '__main__':
    service = P300Service()
    service.initialize_handlers()
    service.app.run(host='localhost', port=8001)
