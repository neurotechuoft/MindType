"""Functions for establishing a test stream that sends out continuous artificial stimulus data"""
import pylsl
import time
import threading
import pandas as pd


def get_raw_template(paths):
    df = pd.DataFrame()
    for path in paths:
        df = df.append(pd.read_csv(path))
    return df


def eeg_publish(signal, outlet):
    """Sends randomly generated markers (row/column number) through the lsl stream outlet."""
    df = get_raw_template(paths=['data/data_2017-02-04-15_45_13.csv',
                                 'data/data_2017-02-04-15_47_49.csv',
                                 'data/data_2017-02-04-15_51_07.csv'])
    print('EEG sending ...')
    while not signal.is_set():
        for i, row in df.iterrows():
            outlet.push_sample([row.TP9, row.AF7, row.AF8, row.TP10])
            time.sleep(0.00390625)
        print('EEG no longer sending.')


def test_eeg_stream():
    """Create and return marker lsl outlet."""
    # create
    info = pylsl.StreamInfo('Muse', 'EEG', 4, 256, 'float32', 'MuseName')
    info.desc().append_child_value("manufacturer", "Muse")
    channels = info.desc().append_child("channels")

    for c in ['TP9-l_ear', 'FP1-l_forehead', 'FP2-r_forehead', 'TP10-r_ear']:
        channels.append_child("channel") \
            .append_child_value("label", c) \
            .append_child_value("unit", "microvolts") \
            .append_child_value("type", "EEG")
    outlet = pylsl.StreamOutlet(info)
    return outlet


def start_eeg_stream(outlet):
    """Starts publishing marker data on the lsl stream in a new thread."""
    kill_signal = threading.Event()
    marker_thread = threading.Thread(target=eeg_publish, name='eeg_publisher', args=(kill_signal, outlet))
    marker_thread.daemon = True
    marker_thread.start()


if __name__ == '__main__':
    test_outlet = test_eeg_stream()
    start_eeg_stream(test_outlet)
    print("looking for a EEG stream")
    streams = pylsl.resolve_byprop('name', 'Muse', timeout=10)
    if len(streams) == 0:
        raise (RuntimeError, "Can't find Markers stream")
    print("Start acquiring data")
    marker_inlet = pylsl.StreamInlet(streams[0])
    while True:
        sample, _ = marker_inlet.pull_sample()
        print(sample)
