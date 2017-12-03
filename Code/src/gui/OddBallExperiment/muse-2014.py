from server import PylibloServer, ServerError
import numpy as np
import bitstring

class Muse2014:

    def __init__(self, address, process_func, port):

        self.address = address
        self.port = port
        self.process_func = process_func
        self.muse_server = None

    def startServer(self):
        try:
            # Trys to connect to server
            self.muse_server = PylibloServer(self.PORT)
        except ServerError, err:
            # print >> sys.stderr, str(err)
            # sys.exit()
            return
        # start server and block server entry
        self.portEdit.setDisabled(True)
        self.btnStartServer.setDisabled(True)
        self.muse_server.start()
        # Start timer Update Graph
        self.timer.start()


    def _unpack_eeg_channel(self, packet):
        """Decode data packet of one eeg channel.
        Each packet is encoded with a 16bit timestamp followed by 12 time
        samples with a 12 bit resolution.
        """
        aa = bitstring.Bits(bytes=packet)
        pattern = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
                   uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"
        res = aa.unpack(pattern)
        packetIndex = res[0]
        data = res[1:]
        # 12 bits on a 2 mVpp range
        data = 0.48828125 * (np.array(data) - 2048)
        return packetIndex, data

    def _handle_eeg(self, handle, data):
        """Calback for receiving a sample.
        sample are received in this oder : 44, 41, 38, 32, 35
        wait until we get 35 and call the data callback
        """
        timestamp = self.time_func()
        index = int((handle - 32) / 3)
        tm, d = self._unpack_eeg_channel(data)

        if self.last_tm == 0:
            self.last_tm = tm - 1

        self.data[index] = d
        self.timestamps[index] = timestamp
        # last data received
        if handle == 35:
            if tm != self.last_tm + 1:
                print("missing sample %d : %d" % (tm, self.last_tm))
            self.last_tm = tm

            # calcultate index of time samples
            idxs = np.arange(0, 12) + self.sample_index
            self.sample_index += 12

            # affect as timestamps
            timestamps = self.reg_params[1] * idxs + self.reg_params[0]

            # push data
            self.process_func(self.data, timestamps)
            self._init_sample()
