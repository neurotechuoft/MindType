"""This script receives raw EEG data from the muse and pushes it to an lsl outlet
Adapted from:
    muse-lsl: https://github.com/alexandrebarachant/muse-lsl.git
    beats-muse: https://github.com/Oishe/beats-muse
"""
from server import *
import time
from pylsl import StreamInfo, StreamOutlet

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


def process(data, timestamp, index):
    outlet.push_sample(data, timestamp)

    # test for response
    if index % 220 == 0:
        print('New Second! @', index, timestamp)


# connect to the server
try:
    muse_server = PylibloServer(PORT, process)
except ServerError:
    muse_server = False

if muse_server:
    muse_server.start()

while 1:
    try:
        time.sleep(1)
    except:
        break

if muse_server:
    muse_server.stop()





