"""Functions for establishing a test stream that sends out continuous artificial stimulus data"""
import pylsl
import time
import random
import threading
import uuid


def repopulate_list(template_list):
    """Creates a shuffled deep copy of a template list."""
    new_list = []
    for item in template_list:
        new_list.append(item)
    random.shuffle(new_list)
    epoch_id = uuid.uuid4()
    return new_list, epoch_id


def marker_publish(signal, outlet, events, log=False):
    """Sends randomly generated markers (row/column number) through the lsl stream outlet."""
    trial_num = len(events)
    generator, epoch_id = repopulate_list(events)
    count = 0
    start_time = pylsl.local_clock()
    if log:
        print('Markers sending ...\n\n\n\n\n')
    while not signal.is_set():
        if generator:
            # generate random marker data
            # status = random.randint(0, 1)
            tmp = generator.pop()
            # chooses the target in the identifiers list
            if tmp == 1:
                event = 1
                if log:
                    print("""
                   AAA
                  A:::A
                 A:::::A
                A:::::::A
               A:::::::::A
              A:::::A:::::A
             A:::::A A:::::A
            A:::::A   A:::::A
           A:::::A     A:::::A
          A:::::AAAAAAAAA:::::A
         A:::::::::::::::::::::A
        A:::::AAAAAAAAAAAAA:::::A
       A:::::A             A:::::A
      A:::::A               A:::::A
     A:::::A                 A:::::A
    AAAAAAA                   AAAAAAA
                    """)
                target = 1
            else:
                event = 0
                if log:
                    print("""
















                    """)
                target = 0

            # increment marker count
            count = count + 1

            t = pylsl.local_clock()
            package = [
                str(t),
                str(target),
                str(trial_num),
                str(epoch_id)
            ]

            # data pushed in form [[identity, target, trial_num], timestamp]
            outlet.push_sample(package)
            # print(' {}' .format(data))
            # print('\n{}\n'.format(letters[tmp])) # print for command line training

            # down time in between sending markers
            time.sleep(0.4)
            # if count % trial_num == 0:
            #     # after trial_num flashes, 1 set of trials complete
            #     end_time = pylsl.local_clock()
            #     if log:
            #         print('\n\n\n\n\ntrial was {} seconds long\n\n\n\n\n'.format(end_time - start_time))
        else:
            generator, epoch_id = repopulate_list(events)
            count = 0
            time.sleep(2)
            start_time = pylsl.local_clock()
    if log:
        print('Markers no longer sending.')


def test_marker_stream():
    """Create and return marker lsl outlet."""
    # create
    info = pylsl.StreamInfo('Markers', 'Markers', 4, 0, 'string', 'mywid32')
    # next make an outlet
    outlet = pylsl.StreamOutlet(info)
    return outlet


def start_marker_stream(outlet, events, log=True):
    """Starts publishing marker data on the lsl stream in a new thread."""
    kill_signal = threading.Event()
    marker_thread = threading.Thread(target=marker_publish, name='marker-generator', args=(kill_signal, outlet, events, log))
    marker_thread.daemon = True
    marker_thread.start()


if __name__ == '__main__':
    test_outlet = test_marker_stream()
    test_events = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    start_marker_stream(test_outlet, test_events, log=True)

    while True:
        time.sleep(5)
