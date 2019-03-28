import socketio
from sanic import Sanic
import random

class P300Client(object):

    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)

    def initialize_handlers(self):
        self.sio.on("train", self.train_handler)
        self.sio.on("predict", self.predict_handler)

    async def train_handler(self, sid, args):
        uuid, timestamp, p300 = args
        acc = random.random()
        results = (uuid, acc)
        return sid, results

    async def predict_handler(self, sid, args):
        uuid, timestamp = args
        p300 = random.choice([True, False])
        score = random.random()
        results = (uuid, p300, score)
        return sid, results



if __name__ == '__main__':
    p300_client = P300Client()
    p300_client.initialize_handlers()
    p300_client.app.run(host='localhost', port=8001)
