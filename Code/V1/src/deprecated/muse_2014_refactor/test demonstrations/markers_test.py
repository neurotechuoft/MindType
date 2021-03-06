"""Functions for establishing a test stream that sends out continuous artificial stimulus data"""
import pylsl
import time
import random
import threading


def repopulate_list(template_list):
    """Creates a shuffled deep copy of a template list."""
    new_list = []
    for item in template_list:
        new_list.append(item)
    random.shuffle(new_list)
    return new_list


def marker_publish(signal, outlet, identifiers):
    """Sends randomly generated markers (row/column number) through the lsl stream outlet."""
    count = 0
    generator = repopulate_list(identifiers)
    start_time = pylsl.local_clock()
    print('Markers sending ...')
    while not signal.is_set():
        if generator:
            # generate random marker data
            status = random.randint(0, 1)
            t = pylsl.local_clock()
            data = [generator.pop(), status]

            # data pushed in form [identity, target, timestamp]
            outlet.push_sample(data, t)
            print(' {}' .format(data))

            # down time in between sending markers
            time.sleep(0.2)

            count = count + 1
            if count % 12 == 0:
                # after 12 flashes, 1 trial complete
                end_time = pylsl.local_clock()
                print('trial was {} seconds long' .format(end_time - start_time))
        else:
            generator = repopulate_list(identifiers)
            time.sleep(4)
            start_time = pylsl.local_clock()
    print('Markers no longer sending.')


def test_marker_stream():
    """Create and return marker lsl outlet."""
    # create
    info = pylsl.StreamInfo('Markers', 'Markers', 2, 0, 'int32', 'mywid32')
    # next make an outlet
    outlet = pylsl.StreamOutlet(info)
    return outlet


def start_marker_stream(outlet, identifiers):
    """Starts publishing marker data on the lsl stream in a new thread."""
    kill_signal = threading.Event()
    marker_thread = threading.Thread(target=marker_publish, name='marker-generator', args=(kill_signal, outlet,
                                                                                           identifiers))
    marker_thread.daemon = True
    marker_thread.start()