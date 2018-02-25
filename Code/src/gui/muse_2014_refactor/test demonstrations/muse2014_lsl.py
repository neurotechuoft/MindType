"""This script receives raw EEG data from the muse and pushes it to an lsl outlet
Useful as a test script.
Adapted from:
    muse-lsl: https://github.com/alexandrebarachant/muse-lsl.git
    beats-muse: https://github.com/Oishe/beats-muse
"""
import Code.src.gui.muse_2014_refactor.server
import time
from pylsl import StreamInfo, StreamOutlet
import Code.src.gui.muse_2014_refactor.stream_rt as st
import Code.src.gui.muse_2014_refactor.analysis_rt as an
import Code.src.gui.muse_2014_refactor.markers_test


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
        print('EEG outlet created')

    # connect to the server
    try:
        muse_server = Code.src.gui.muse_2014_refactor.server.PylibloServer(PORT, Code.src.gui.muse_2014_refactor.server.process, outlet)
    except Code.src.gui.muse_2014_refactor.server.ServerError:
        raise ValueError('Cannot create PylibloServer Object')
    if muse_server:
        muse_server.connect()

    # establish test marker stream; for test purposes only
    outlet = Code.src.gui.muse_2014_refactor.markers_test.test_marker_stream()
    print('marker stream started')

    # connect to inlets
    # Create MuseEEGStream object
    eeg_stream = st.MuseEEGStream()

    # Create Marker Stream object
    marker_stream = st.MarkerStream()

    # ensure streams are streaming data before accessing (there should be a better way to do this)
    time.sleep(3)

    # start marker test trial
    Code.src.gui.muse_2014_refactor.markers_test.start_marker_stream(outlet)
    # time for marker object to collect data
    time.sleep(3.4)
    # (When trial END signal arrives) make an epoch of the last 12 flashes and 1000 ms after
    rt_filter = an.RTAnalysis(marker_stream, eeg_stream, data_duration=3.6)
    rt_filter.start()

    while 1:
        try:
            time.sleep(1)
        except:
            break

    muse_server.stop()


if __name__ == '__main__':
    main()






