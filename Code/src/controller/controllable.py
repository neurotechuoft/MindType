from controller import Controller
from MESSAGE import Message


class Controllable(object):

    def __init__(self):
        # Multithreading
        self.controller = Controller()
        self.__paused__ = True
        self.__exit__ = False

    def control(self):
        message = self.controller.read()
        self.execute_message_instruction(message)

    def execute_message_instruction(self, message):
        if message is Message.PAUSE:
            self.pause()
        elif message is Message.START:
            self.resume()
        elif message is Message.EXIT:
            self.exit()

    def is_paused(self):
        return self.__paused__

    def is_exit(self):
        return self.__exit__

    def pause(self):
        self.__paused__ = True

    def resume(self):
        self.__paused__ = False

    def exit(self):
        self.__exit__ = True
