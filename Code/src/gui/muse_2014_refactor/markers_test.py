"""Functions for establishing a test stream that sends out artificial P300 keyboard stimulus data"""

import pylsl
import time
import random
import threading


def marker_publish(signal, outlet):
    count = 0
    start_time = pylsl.local_clock()
    while not signal.is_set():
        # generate random marker data
        data = [random.randint(0, 1)]
        t = pylsl.local_clock()
        if count < 12:
            outlet.push_sample(data, t)
        if count==0:
            print('started markers trial')
        count = count + 1
        time.sleep(0.2)
        # after 12 flashes, end the trial
        if count==12:
            print('end of markers trial')
            end_time = pylsl.local_clock()
            print('trial was {} seconds long' .format(end_time - start_time))


def test_marker_stream():
    # create
    info = pylsl.StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
    # next make an outlet
    outlet = pylsl.StreamOutlet(info)
    return outlet


def start_marker_stream(outlet):
    kill_signal = threading.Event()
    marker_thread = threading.Thread(target=marker_publish, name='marker-generator', args=(kill_signal, outlet))
    marker_thread.daemon = True
    marker_thread.start()