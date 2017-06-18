import json
import sys
import threading
import time

import zmq

from biosignals.P300 import P300


class Interface:
    def __init__(self, verbose=False):
        context = zmq.Context()
        self._socket = context.socket(zmq.PAIR)
        self._socket.connect("tcp://localhost:3004")

        self.verbose = verbose

        if self.verbose:
            print("Client Ready!")

        # Send a quick message to tell node process we are up and running
        self.send(json.dumps({
            'action': 'started',
            'command': 'status',
            'message': time.time()*1000.0
        }))

    def send(self, msg):
        """
        Sends a message to TCP server
        :param msg: str
            A string to send to node TCP server, could be a JSON dumps...
        :return: None
        """
        if self.verbose:
            print('<- out ' + msg)
        self._socket.send(msg)
        return

    def recv(self):
        """
        Checks the ZeroMQ for data
        :return: str
            String of data
        """
        return self._socket.recv()


def process(biosignal):
    # stop = False
    # while not stop:
    #     biosignal.process()
    #
    #     if biosignal.is_stop():
    #         stop = True
    exit = False

    while not exit:
        if not biosignal.is_stop():
            biosignal.process()
        if biosignal.is_exit():
            exit = True


def main(argv):
    nb_chan = 8
    verbose = True
    biosignal = P300(256)
    # Create a new python interface.
    interface = Interface(verbose=verbose)
    process_thread = threading.Thread(target=process, args=[biosignal])

    num = 0
    while True:
        sample = interface.recv()
        biosignal.update(sample)
        if num == 0:
            process_thread.start()
            num += 1

if __name__ == '__main__':
    main(sys.argv[1:])
