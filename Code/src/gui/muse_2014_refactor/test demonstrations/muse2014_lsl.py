"""This script receives raw EEG data from the muse and pushes it to an lsl outlet. Gets data from
incoming stimuli events and performs analysis on them.
Adapted from:
    muse-lsl: https://github.com/alexandrebarachant/muse-lsl.git
    beats-muse: https://github.com/Oishe/beats-muse
"""
import Code.src.gui.muse_2014_refactor.server as server
import time
from pylsl import StreamInfo, StreamOutlet
import Code.src.gui.muse_2014_refactor.stream_rt as st
import Code.src.gui.muse_2014_refactor.analysis_rt as an
import markers_test


def main():
    PORT = '1234'
    info = StreamInfo('Muse', 'EEG', 4, 220, 'float32',
                      'MuseName')

    info.desc().append_child_value("manufacturer", "Muse")
    channels = info.desc().append_child("channels")

    for c in ['TP9-l_ear', 'FP1-l_forehead', 'FP2-r_forehead', 'TP10-r_ear']:
        channels.append_child("channel") \
            .append_child_value("label", c) \
            .append_child_value("unit", "microvolts") \
            .append_child_value("type", "EEG")
    # specify info, chunk size (each push yields one chunk), and maximum buffered data
    outlet = StreamOutlet(info, 1, 360)
    if outlet:
        print('EEG outlet created.')

    # connect to the server
    try:
        muse_server = server.PylibloServer(PORT, server.process, outlet)
    except server.ServerError:
        raise ValueError('Cannot create PylibloServer Object.')
    if muse_server:
        muse_server.connect()
    else:
        print('No muse connection.')
        return

    # establish test marker stream; for test purposes only
    outlet = markers_test.test_marker_stream()
    # 0 - 11 for 12 rows/columns
    identifiers = range(0, 12, 1)
    print('Marker outlet created.')

    # connect to inlets
    # Create MuseEEGStream object
    eeg_stream = st.MuseEEGStream()

    # Create Marker Stream object
    marker_stream = st.MarkerStream()

    # data_duration = (flash time + pause time) * number of flashes + P300 detection time (0.75 s)
    data_duration = 3.4

    # Create analysis object
    analysis = an.RTAnalysis(marker_stream, eeg_stream, 'classifier.pkl', event_time=0.4, train='True', train_epochs=48)

    # ensure eeg stream is receiving data before accessing and starting stimuli
    while not eeg_stream.data:
        time.sleep(0.1)

    markers_test.start_marker_stream(outlet, identifiers)
    analysis.start()

    while 1:
        try:
            time.sleep(1)
        except:
            break

    muse_server.stop()


if __name__ == '__main__':
    main()







