from MESSAGE import Message
from controllable import Controllable


class Processor(Controllable):

    def __init__(self, biosignals):
        Controllable.__init__(self)
        self.biosignals = biosignals

    def process(self):
        self.control()

        if self.is_exit():
            return Message.EXIT
        elif self.is_paused():
            return Message.IDLE

        for biosignal in self.biosignals:
            biosignal.process()

        return Message.ACTIVE