import socketio
from sanic import Sanic
import random
import json

class P300Client(object):

    def __init__(self):
        self.sio = socketio.AsyncServer(async_mode='sanic')
        self.app = Sanic()
        self.sio.attach(self.app)

    def initialize_handlers(self):
        self.sio.on("train", self.train_handler)
        self.sio.on("predict", self.predict_handler)

        self.sio.on("login", self.login_handler)
        self.sio.on("logout", self.logout_handler)
        self.sio.on("register", self.register_handler)

    async def login_handler(self, sid, args):
        return sid, random.choice([True, False])

    async def logout_handler(self, sid, args):
        return sid, random.choice([True, False])

    async def register_handler(self, sid, args):
        return sid, random.choice([True, False])

    async def train_handler(self, sid, args):
        uuid, timestamp, p300 = args
        acc = random.random()
        acc = random.choice([acc, None])
        return sid, acc

    async def predict_handler(self, sid, args):
        print(args)
        uuid, timestamp = args
        p300 = random.choice([True, False])
        score = random.random()
        results = {'uuid': uuid, 'p300': p300, 'score': score}
        print(sid)
        return sid, json.dumps(results)



if __name__ == '__main__':
    p300_client = P300Client()
    p300_client.initialize_handlers()
    p300_client.app.run(host='localhost', port=8002)
