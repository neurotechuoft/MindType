# from Queue import Queue
from collections import deque

from MESSAGE import Message


class Controller:

    def __init__(self):
        self.msg_queue = deque(maxlen=10)
        self.send(Message.PAUSE)

    def send(self, msg):
        self.msg_queue.append(msg)

    def read(self):
        return self.msg_queue.popleft() if self.msg_queue else None

    def peek(self):
        msg = None

        if self.msg_queue:
            msg = self.read()

            if msg:
                self.msg_queue.appendleft(msg)

        return msg