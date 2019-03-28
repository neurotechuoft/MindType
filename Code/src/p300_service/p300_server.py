from sanic import Sanic
import socketio

from eeg_stream import EEGStream
from marker_stream import MarkerStream
from ml_stream import MLStream
import ml

import numpy as np
from sklearn.model_selection import train_test_split

# for testing
import random


class P300Service:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)

        self.clf = None
        self.inputs = []
        self.targets = []

        self.last_uuid = -1
        self.last_acc = 0.

    async def load_classifier(self, sid):
        try:
            self.clf = ml.load(f"tests/data/classifier.pkl")
        except FileNotFoundError:
            raise Exception(f"Cannot load classifier")

    async def train_classifier(self, sid, args):
        uuid, eeg_data, p300 = args
        self.inputs.append(np.array(eeg_data))
        self.targets.append(np.array(p300))

        if len(self.targets) % 10 == 0 and len(self.targets) > 70:
            X = np.array(self.inputs)
            y = np.array(self.targets)

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

            # Note in Barachant's ipynb, 'erpcov_mdm' performed best. 'vect_lr' is the
            # universal one for EEG data.
            self.clf = ml.ml_classifier(X_train, y_train, pipeline='vect_lr')
            acc = self.clf.score(X_test, y_test)
            ml.save(f"tests/data/clf.pkl", classifier)

            self.last_uuid = uuid
            self.last_acc = acc

        results = (self.last_uuid, self.last_acc)
        return sid, results

    async def retrieve_prediction_results(self, sid, args):
        uuid, data = args
        p300 = self.clf.predict(data)
        score = 1
        results = (uid, p300, score)
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
