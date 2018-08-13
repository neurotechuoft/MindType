"""This script receives raw EEG data from the muse and pushes it to an lsl outlet.
Adapted from:
    muse-lsl: https://github.com/alexandrebarachant/muse-lsl.git
    beats-muse: https://github.com/Oishe/beats-muse
"""
import Code.src.muse_2014_refactor.server as server
import time
from pylsl import StreamInfo, StreamOutlet
import Code.src.muse_2014_refactor.stream_rt as st


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

    # create a pylsl outlet; specify info, chunk size (each push yields one chunk), and maximum buffered data
    outlet = StreamOutlet(info, 1, 360)
    if outlet:
        print('EEG outlet created.')

    # connect to the server; start pushing muse data to the pylsl outlet
    try:
        muse_server = server.PylibloServer(PORT, server.process, outlet)
    except server.ServerError:
        raise ValueError('Cannot create PylibloServer Object.')
    if muse_server:
        muse_server.connect()
    else:
        print('No muse connection.')
        return

    # connect to inlets
    # Create MuseEEGStream object
    eeg_stream = st.MuseEEGStream()

    # ensure eeg stream is receiving data before trying to access data
    while not eeg_stream.data:
        time.sleep(0.1)

    for i in range(1000):
        try:
            # print the eeg data every second
            print(eeg_stream.data[-1])
            time.sleep(1)
        except:
            break

    muse_server.stop()


if __name__ == '__main__':
    main()







