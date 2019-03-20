from sanic import Sanic
import socketio
from eeg_stream import EEGStream
from marker_stream import MarkerStream
from ml_stream import MLStream

# for testing
import random


class P300Service:
    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)

    async def retrieve_prediction_results(self, sid):
        if sid in self.ml_streams:
            ml_stream = self.ml_streams[sid]
        else:
            raise Exception("Cannot start ML stream with sid {}".format(sid))
        results = ml_stream.predictions
        await self.sio.emit("retrieve_prediction_results", sid, results)

    # for testing
    async def retrieve_prediction_results_test(self, sid, args):
        uid, ts, data = args
        p300 = random.choice([True, False])
        results = (uid, ts, p300)
        return sid, results


    def initialize_handlers(self):
        self.sio.on("retrieve_prediction_results", self.retrieve_prediction_results_test)


if __name__ == '__main__':
    service = P300Service()
    service.initialize_handlers()
    service.app.run(host='localhost', port=8001)
