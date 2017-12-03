# from Queue import Queue
from collections import deque

from MESSAGE import Message


class Controller:
    """
        Object that receives messages and stores them from oldest to newest.
    """

    def __init__(self):
        self.__msg_queue__ = deque(maxlen=10)
        self.send(Message.PAUSE)

    def send(self, msg):
        """
        Send a message to the controller.

        Args:
            msg (Message): message

        Returns:

        """
        self.__msg_queue__.append(msg)

    def read(self):
        """
        Return latest message, and remove from controller.
        Returns: Message

        """
        return self.__msg_queue__.popleft() if self.__msg_queue__ else None

    def peek(self):
        """
        See latest message without removing from controller.
        Returns: Message

        """
        msg = None

        if self.__msg_queue__:
            msg = self.read()

            if msg:
                self.__msg_queue__.appendleft(msg)

        return msg

    def search(self, message):
        """
        Search for a particular message in the controller
        Args:
            message (Message): message to search

        Returns: bool

        """
        return str(message) in self.__str__()

    def __str__(self):
        return self.__msg_queue__.__str__()