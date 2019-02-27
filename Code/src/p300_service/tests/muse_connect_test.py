"""This script receives raw EEG data from the muse and pushes it to an lsl outlet.
Adapted from:
    muse-lsl: https://github.com/alexandrebarachant/muse-lsl.git
    beats-muse: https://github.com/Oishe/beats-muse
"""
import time
import pylsl
from p300_service import eeg_stream, marker_stream, ml_stream
from tests.test_marker_publisher import test_marker_stream, start_marker_stream
from tests.test_eeg_publisher import test_eeg_stream, start_eeg_stream


def main(random_eeg_data=False):
    if random_eeg_data:
        eeg_outlet = test_eeg_stream()
        start_eeg_stream(eeg_outlet)

    eeg = eeg_stream.EEGStream(thread_name='test_eeg')
    eeg.lsl_connect()

    # ensure eeg stream is receiving data before trying to access data
    while not eeg.data:
        time.sleep(0.1)

    # Create Marker Stream object
    marker_outlet = test_marker_stream()
    marker = marker_stream.MarkerStream(thread_name='test_marker')
    marker.lsl_connect()
    time.sleep(5)
    events = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    start_marker_stream(marker_outlet, events)

    while not marker.data:
        time.sleep(0.1)

    # Create analysis object; this example trains a new classifier on the incoming data
    analysis = ml_stream.MLStream(
        m_stream=marker,
        eeg_stream=eeg,
        classifier_path='classifier.pkl',
        test_path='classifier.pkl',
        event_time=0.4,
        train='True',
        train_epochs=120
    )
    analysis.start()

    while True:
        print('marker', marker.data[-1])
        time.sleep(1)


if __name__ == '__main__':
    main(random_eeg_data=True)







