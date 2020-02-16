"""
Core OpenBCI object for handling connections and samples from the board.

EXAMPLE USE:

def handle_sample(sample):
    print(sample.channel_data)

board = OpenBCIBoard()
board.print_register_settings()
board.start_streaming(handle_sample)

NOTE: If daisy modules is enabled, the callback will occur every two samples, hence "packet_id" will only contain even
numbers. As a side effect, the sampling rate will be divided by 2.

FIXME: at the moment we can just force daisy mode, do not check that the module is detected.
TODO: enable impedance

"""

import serial
import struct
import numpy as np
import time
import timeit
import atexit
import logging
import threading
import sys
import pdb
import glob

# cython
import openbci_board.openbci_board.v3functions as cyfunc

from biosignals.biosignal import BioSignal

SAMPLE_RATE = 250.0     # Hz
START_BYTE = b'\xA0'    # start of data packet
END_BYTE = 0xC0         # end of data packet
ADS1299_Vref = 4.5      # reference voltage for ADC in ADS1299.  set by its hardware
ADS1299_gain = 24.0     # assumed gain setting for ADS1299.  set by its Arduino code
scale_fac_uVolts_per_count = ADS1299_Vref / float((pow(2, 23) - 1)) / ADS1299_gain * 1000000.
scale_fac_accel_G_per_count = 0.002 / (pow(2, 4))  # assume set to +/4G, so 2 mG

'''
Commands for in SDK http://docs.openbci.com/software/01-Open BCI_SDK:

command_stop = "s"
command_startText = "x"
command_startBinary = "b"
command_startBinary_wAux = "n"
command_startBinary_4chan = "v"
command_activateFilters = "F"
command_deactivateFilters = "g"

command_deactivate_channel = {"1", "2", "3", "4", "5", "6", "7", "8"}           # 1-8 (on keyboard)
command_activate_channel = {"q", "w", "e", "r", "t", "y", "u", "i"}             # q-i (on keyboard)

command_activate_leadoffP_channel = {"!", "@", "#", "$", "%", "^", "&", "*"}    # shift + 1-8 (on keyboard)
command_deactivate_leadoffP_channel = {"Q", "W", "E", "R", "T", "Y", "U", "I"}  # shift + q-i (on keyboard)

command_activate_leadoffN_channel = {"A", "S", "D", "F", "G", "H", "J", "K"}    # shift + a-k (on keyboard)
command_deactivate_leadoffN_channel = {"Z", "X", "C", "V", "B", "N", "M", "<"}  # shift + z-, (on keyboard)

command_biasAuto = "`"
command_biasFixed = "~"
'''


class OpenBCIBoard(object):
    """ Handle a connection to an OpenBCI board.

    Args:
        port: The port to connect to.
        baud: The baud of the serial connection.
        daisy: Enable or disable daisy module and 16 chans readings
        aux, impedance: unused, for compatibility with ganglion API
    """

    def __init__(self, port=None, baud=115200, filter_data=True,
                 scaled_output=True, daisy=False, aux=False, impedance=False,
                 log=True, timeout=None):

        self.log = log  # print_incoming_text needs log
        self.streaming = False
        self.baudrate = baud
        self.timeout = timeout
        if not port:
            port = self.find_port()
        self.port = port
        # might be handy to know API
        self.board_type = "cyton"
        print("Connecting to V3 at port %s" % port)
        self.ser = serial.Serial(port=port, baudrate=baud, timeout=timeout)

        print("Serial established...")

        time.sleep(2)
        # Initialize 32-bit board, doesn't affect 8bit board
        self.ser.write(b'v')

        # wait for device to be ready
        time.sleep(1)
        self.print_incoming_text()

        self.streaming = False
        self.filtering_data = filter_data
        self.scaling_output = scaled_output
        self.eeg_channels_per_sample = 8  # number of EEG channels per sample *from the board*
        self.aux_channels_per_sample = 3  # number of AUX channels per sample *from the board*
        self.imp_channels_per_sample = 0  # impedance check not supported at the moment
        self.read_state = 0
        self.daisy = daisy
        self.last_odd_sample = OpenBCISample(-1, [], [])  # used for daisy
        self.log_packet_count = 0
        self.attempt_reconnect = False
        self.last_reconnect = 0
        self.reconnect_freq = 5
        self.packets_dropped = 0

        # Disconnects from board when terminated
        atexit.register(self.disconnect)

    def getBoardType(self):
        """ Returns the version of the board """
        return self.board_type

    def setImpedance(self, flag):
        """ Enable/disable impedance measure. Not implemented at the moment on Cyton. """
        return

    def ser_write(self, b):
        """Access serial port object for write"""
        self.ser.write(b)

    def ser_read(self):
        """Access serial port object for read"""
        return self.ser.read()

    def ser_inWaiting(self):
        """Access serial port object for inWaiting"""
        return self.ser.inWaiting()

    def getSampleRate(self):
        if self.daisy:
            return SAMPLE_RATE / 2
        else:
            return SAMPLE_RATE

    def getNbEEGChannels(self):
        if self.daisy:
            return self.eeg_channels_per_sample * 2
        else:
            return self.eeg_channels_per_sample

    def getNbAUXChannels(self):
        return self.aux_channels_per_sample

    def getNbImpChannels(self):
        return self.imp_channels_per_sample

    def start_streaming(self, callback, lapse=-1, biosignals=None):
        """ Start handling streaming data from the board. Call a provided callback
        for every single sample that is processed (every two samples with daisy module).

        :param callback: A callback function -- or a list of functions -- that will receive a single
        argument of the OpenBCISample object captured.
        :param lapse: optional cap on streaming time
        :param biosignals: biosignal object
        """
        if not self.streaming:
            self.ser.write(b'b')
            self.streaming = True

        start_time = timeit.default_timer()

        # Enclose callback funtion in a list if it comes alone
        if not isinstance(callback, list):
            callback = [callback]

        # Initialize check connection
        self.check_connection()

        while self.streaming:

            # read current sample
            sample = self._read_serial_binary()
            # if a daisy module is attached, wait to concatenate two samples (main board + daisy)
            if self.daisy:
                # odd sample: daisy sample, save for later
                if ~sample.id % 2:
                    self.last_odd_sample = sample
                # even sample: concatenate and send if last sample was the fist part, otherwise drop the packet
                elif sample.id - 1 == self.last_odd_sample.id:
                    # aux data is average between the two samples, as the channel samples are averaged by the board
                    avg_aux_data = list((np.array(sample.aux_data) + np.array(
                        self.last_odd_sample.aux_data)) / 2)
                    whole_sample = OpenBCISample(sample.id,
                                                 sample.channel_data + self.last_odd_sample.channel_data,
                                                 avg_aux_data)
                    for call in callback:
                        if biosignals is not None:
                            call(whole_sample, biosignals)
                        else:
                            call(whole_sample)
            else:
                for call in callback:
                    if biosignals is not None:
                        call(sample, biosignals)
                    else:
                        call(sample)

            # stop streaming after lapse amount of time
            if timeit.default_timer() - start_time > lapse > 0:
                self.stop()
            if self.log:
                self.log_packet_count = self.log_packet_count + 1

    def start_board(self, start_time, biosignals, lapse=-1):
        """ Start handling streaming data from the board. Call a provided callback
        for every single sample that is processed (every two samples with daisy module).

        :param callback: A callback function -- or a list of functions -- that will receive a single
        argument of the OpenBCISample object captured.
        :param lapse: optional cap on streaming time
        :param biosignals: biosignal object
        """
        if not self.streaming:
            self.ser.write(b'b')
            self.streaming = True

        start_time = timeit.default_timer()
        
        print(type(biosignals))
        print(type(biosignals[0]))

        # Initialize check connection
        self.check_connection()
        
        print("Starting to stream")

        while self.streaming:

            # read current sample
            print("OpenBCI reading sample...")
            sample = self._read_serial_binary()
            print("OpenBCI finished reading sample")
            # if a daisy module is attached, wait to concatenate two samples (main board + daisy)
            if self.daisy:
                # odd sample: daisy sample, save for later
                if ~sample.id % 2:
                    self.last_odd_sample = sample
                # even sample: concatenate and send if last sample was the fist part, otherwise drop the packet
                elif sample.id - 1 == self.last_odd_sample.id:
                    # aux data is average between the two samples, as the channel samples are averaged by the board
                    avg_aux_data = list((np.array(sample.aux_data) + np.array(self.last_odd_sample.aux_data)) / 2)
                    whole_sample = OpenBCISample(sample.id,
                                                 sample.channel_data + self.last_odd_sample.channel_data,
                                                 avg_aux_data)
                    # UPDATE OBJECTS
                    if biosignals is not None:
                        for biosignal in biosignals:
                            if isinstance(biosignal, BioSignal):
                                # print("OpenBCI updating biosignal with" + str(whole_sample))
                                biosignal.update(self.parse_sample(whole_sample, start_time))
                            else:
                                print("Object isn't a biosignal!")
                    else:
                        print("There are no biosignals!")
            else:
                # UPDATE OBJECTS
                if biosignals is not None:
                    for biosignal in biosignals:
                        if isinstance(biosignal, BioSignal):
                            # print("OpenBCI updating biosignal with" + str(sample))
                            biosignal.update(self.parse_sample(sample, start_time))
                        else:
                            print("Object isn't a biosignal!")
                else:
                    print("There are no biosignals!")
            
            # print("Streamed biosignal")

            # stop streaming after lapse amount of time
            if timeit.default_timer() - start_time > lapse > 0:
                self.stop()
            if self.log:
                self.log_packet_count = self.log_packet_count + 1

    def parse_sample(self, sample, start_time):
        t = timeit.default_timer() - start_time

        # print timeSinceStart|Sample Id
        # if self.verbose:
        # 	print("CSV: %f | %d" % (t, sample.id))
        row = ''
        row += str(t)
        row += ","

        row += str(sample.id)
        row += ","

        for i in sample.channel_data:
            row += str(i)
            row += ","

        data = row.split(",")

        return data

    """

        PARSER:
        Parses incoming data packet into OpenBCISample.
        Incoming Packet Structure:
        Start Byte(1)|Sample ID(1)|Channel Data(24)|Aux Data(6)|End Byte(1)
        0xA0|0-255|8, 3-byte signed ints|3 2-byte signed ints|0xC0

    """

    # cythonfn.pyx
    def _read_serial_binary(self, max_bytes_to_skip=3000):
        """ Main process: unpacks bytes from self.ser and creates OpenBCISample object from unpacked bytes.
        See incoming packet structure above. Warns user if unpacked data is unexpected.

        :param max_bytes_to_skip: allows this many bytes to be dropped before function stops operating
        :return: OpenBCISample object
        """

        def read(n):
            """ Reads n bytes from self.ser and returns them """
            bb = self.ser.read(n)

            # adds sanity check to serial.read() -- makes sure self.ser contains bytes to read
            if not bb:
                self.warn('Device appears to be stalled. Quitting...')
                sys.exit()
                raise Exception('Device Stalled')
                sys.exit()
                return '\xFF'
            else:
                return bb

        log_bytes_in = ""
        
        for rep in range(max_bytes_to_skip):

            # ---------Start Byte & ID---------
            # reads bytes until it finds START_BYTE, warns client if there are bytes before, and starts
            # process at START_BYTE
            if self.read_state == 0:
                if read(1) == START_BYTE:

                    # found rep bytes before START_BYTE
                    if rep != 0:
                        self.warn('Skipped %d bytes before start found' % rep)
                        rep = 0

                    packet_id = struct.unpack('B', read(1))[0]  # packet id goes from 0-255
                    log_bytes_in = str(packet_id)

                    # start at START_BYTE, regardless of if bytes before
                    self.read_state = 1

            # ---------Channel Data---------
            # reads from struct and adds channel data to channel in order of channel
            elif self.read_state == 1:

		        # get channel data for 8 channels * 3 bytes per channel
                channel_data = cyfunc.get_channel_data(read(24), self.scaling_output, self.eeg_channels_per_sample, scale_fac_uVolts_per_count)

                self.read_state = 2

            # ---------Accelerometer Data---------
            # same process as above but instead adding accelerometer data to aux_data
            elif self.read_state == 2:
                
                # get aux data for 3 aux channels * 2 bytes per channel
                aux_data = cyfunc.get_aux_data(read(6), self.scaling_output, self.aux_channels_per_sample, scale_fac_accel_G_per_count)

                self.read_state = 3

            # ---------End Byte---------
            # creates OpenBCISample from channel_data and aux_data and returns it and detects if packets
            # are dropped (ie. if last byte is not END_BYTE, data must have been lost)
            elif self.read_state == 3:
                val = struct.unpack('B', read(1))[0]
                log_bytes_in = log_bytes_in + '|' + str(val)
                self.read_state = 0  # read next packet

                if val == END_BYTE:
                    sample = OpenBCISample(packet_id, channel_data, aux_data)
                    self.packets_dropped = 0
                    return sample
                else:
                    self.warn("ID:<%d> <Unexpected END_BYTE found <%s> instead of <%s>" % (packet_id, val, END_BYTE))
                    logging.debug(log_bytes_in)
                    self.packets_dropped = self.packets_dropped + 1

    """

        Clean Up (atexit)

    """

    def stop(self):
        print("Stopping streaming...\nWait for buffer to flush...")
        self.streaming = False
        self.ser.write(b's')
        if self.log:
            logging.warning('sent <s>: stopped streaming')

    def disconnect(self):
        if self.streaming:
            self.stop()
        if self.ser.isOpen():
            print("Closing Serial...")
            self.ser.close()
            logging.warning('serial closed')

    """

        SETTINGS AND HELPERS

    """

    def warn(self, text):
        """ Stardard warning when program encounters something unexpected, or needs to give client
        a message

        :param text: description of the error
        :return: None
        """
        if self.log:
            # log how many packets where sent succesfully in between warnings
            if self.log_packet_count:
                logging.info(
                    'Data packets received:' + str(self.log_packet_count))
                self.log_packet_count = 0
            logging.warning(text)
        print("Warning: %s" % text)

    def print_incoming_text(self):
        """ When starting the connection and self.ser input buffer is not empty, print all the debug data
        until a line with the end sequence '$$$'.

        :return: None
        """
        # Wait for device to send data
        time.sleep(1)

        if self.ser.inWaiting():
            line = ''
            c = ''
            # Look for end sequence $$$
            while '$$$' not in line:
                # we're supposed to get UTF8 text, but the board might behave otherwise
                c = self.ser.read().decode('utf-8', errors='replace')
                line += c
            print(line)
        else:
            self.warn("No Message")

    def openbci_id(self, serial):
        """ When automatically detecting port, parse the serial return for the 'OpenBCI' ID.

        :param serial: serial to search through
        :return: True if 'OpenBCI" ID is found, False otherwise
        """
        # Wait for device to send data
        time.sleep(2)

        if serial.inWaiting():
            line = ''
            # Look for end sequence $$$
            while '$$$' not in line:
                # we're supposed to get UTF8 text, but the board might behave otherwise
                c = serial.read().decode('utf-8', errors='replace')
                line += c
            if "OpenBCI" in line:
                return True
        return False

    def print_register_settings(self):
        """ Prints incoming text (debug data) (?) """
        self.ser.write(b'?')
        time.sleep(0.5)
        self.print_incoming_text()

    def print_bytes_in(self):
        """ DEBBUGING: Prints individual incoming bytes. """
        if not self.streaming:
            self.ser.write(b'b')
            self.streaming = True
        while self.streaming:
            print(struct.unpack('B', self.ser.read())[0])

    '''Incoming Packet Structure:
    Start Byte(1)|Sample ID(1)|Channel Data(24)|Aux Data(6)|End Byte(1)
    0xA0|0-255|8, 3-byte signed ints|3 2-byte signed ints|0xC0'''

    def print_packets_in(self):
        """ DEBUGGING: Gathers and prints individual incoming packets. Format for gathering into packets
        is similar to _read_serial_binary above. See incoming packet structure above."""

        # needs fixing (referenced skipped_str before assignment, assumes not daisy)
        while self.streaming:
            b = struct.unpack('B', self.ser.read())[0]

            # next up is the beginning of a packet -- start creating a str representation of packet
            if b == START_BYTE:
                self.attempt_reconnect = False

                # if there are any bytes we skipped before the start byte (?)
                if skipped_str:
                    logging.debug('SKIPPED\n' + skipped_str + '\nSKIPPED')
                    skipped_str = ''

                # start byte
                packet_str = "%03d" % b + '|'
                b = struct.unpack('B', self.ser.read())[0]
                packet_str = packet_str + "%03d" % b + '|'

                # data channels
                for i in range(24 - 1):
                    b = struct.unpack('B', self.ser.read())[0]
                    packet_str = packet_str + '.' + "%03d" % b

                b = struct.unpack('B', self.ser.read())[0]
                packet_str = packet_str + '.' + "%03d" % b + '|'

                # aux channels
                for i in range(6 - 1):
                    b = struct.unpack('B', self.ser.read())[0]
                    packet_str = packet_str + '.' + "%03d" % b

                b = struct.unpack('B', self.ser.read())[0]
                packet_str = packet_str + '.' + "%03d" % b + '|'

                # end byte
                b = struct.unpack('B', self.ser.read())[0]

                # Valid Packet -- print out packet
                if b == END_BYTE:
                    packet_str = packet_str + '.' + "%03d" % b + '|VAL'
                    print(packet_str)
                    # logging.debug(packet_str)

                # Invalid Packet -- will attempt to reconnect
                else:
                    packet_str = packet_str + '.' + "%03d" % b + '|INV'
                    # Reset
                    self.attempt_reconnect = True

            # add a byte to skipped_str if the next self.ser.read does not give START_BYTE
            else:
                print(b)
                if b == END_BYTE:
                    skipped_str = skipped_str + '|END|'
                else:
                    skipped_str = skipped_str + "%03d" % b + '.'

            # reconnect after some time if in attempting to reconnect state
            if self.attempt_reconnect and (timeit.default_timer() - self.last_reconnect) > self.reconnect_freq:
                self.last_reconnect = timeit.default_timer()
                self.warn('Reconnecting')
                self.reconnect()

    def check_connection(self, interval=2, max_packets_to_skip=10):
        """ Reconnects if too many packets dropped. Checks connection after interval seconds again by
         calling itself. Does nothing if not streaming.

        :param interval: time interval after with to attempt to reconnect again
        :param max_packets_to_skip: number of packets before attempt at reconnect
        :return: None
        """
        # stop checking when we're no longer streaming
        if not self.streaming:
            return

        # check number of dropped packages and establish connection problem if too large
        if self.packets_dropped > max_packets_to_skip:
            # if error, attempt to reconect
            self.reconnect()
        # run check_connection again after interval seconds
        threading.Timer(interval, self.check_connection).start()

    def reconnect(self):
        """ Reconnects and starts streaming """
        self.packets_dropped = 0
        self.warn('Reconnecting')
        self.stop()
        time.sleep(0.5)
        self.ser.write(b'v')
        time.sleep(0.5)
        self.ser.write(b'b')
        time.sleep(0.5)
        self.streaming = True
        # self.attempt_reconnect = False

    def enable_filters(self):
        """ Adds a filter at 60hz to cancel out ambient electrical noise """
        self.ser.write(b'f')
        self.filtering_data = True

    def disable_filters(self):
        """ Removes above filter """
        self.ser.write(b'g')
        self.filtering_data = False

    def test_signal(self, signal):
        """ Enable / disable test signal """
        if signal == 0:
            self.ser.write(b'0')
            self.warn("Connecting all pins to ground")
        elif signal == 1:
            self.ser.write(b'p')
            self.warn("Connecting all pins to Vcc")
        elif signal == 2:
            self.ser.write(b'-')
            self.warn("Connecting pins to low frequency 1x amp signal")
        elif signal == 3:
            self.ser.write(b'=')
            self.warn("Connecting pins to high frequency 1x amp signal")
        elif signal == 4:
            self.ser.write(b'[')
            self.warn("Connecting pins to low frequency 2x amp signal")
        elif signal == 5:
            self.ser.write(b']')
            self.warn("Connecting pins to high frequency 2x amp signal")
        else:
            self.warn(
                "%s is not a known test signal. Valid signals go from 0-5" % signal)

    def set_channel(self, channel, toggle_position):
        """ Enable / disable channels. See commands at top of file. """

        # Commands to set toggle to on position
        if toggle_position == 1:
            if channel is 1:
                self.ser.write(b'!')
            if channel is 2:
                self.ser.write(b'@')
            if channel is 3:
                self.ser.write(b'#')
            if channel is 4:
                self.ser.write(b'$')
            if channel is 5:
                self.ser.write(b'%')
            if channel is 6:
                self.ser.write(b'^')
            if channel is 7:
                self.ser.write(b'&')
            if channel is 8:
                self.ser.write(b'*')
            if channel is 9 and self.daisy:
                self.ser.write(b'Q')
            if channel is 10 and self.daisy:
                self.ser.write(b'W')
            if channel is 11 and self.daisy:
                self.ser.write(b'E')
            if channel is 12 and self.daisy:
                self.ser.write(b'R')
            if channel is 13 and self.daisy:
                self.ser.write(b'T')
            if channel is 14 and self.daisy:
                self.ser.write(b'Y')
            if channel is 15 and self.daisy:
                self.ser.write(b'U')
            if channel is 16 and self.daisy:
                self.ser.write(b'I')

        # Commands to set toggle to off position
        elif toggle_position == 0:
            if channel is 1:
                self.ser.write(b'1')
            if channel is 2:
                self.ser.write(b'2')
            if channel is 3:
                self.ser.write(b'3')
            if channel is 4:
                self.ser.write(b'4')
            if channel is 5:
                self.ser.write(b'5')
            if channel is 6:
                self.ser.write(b'6')
            if channel is 7:
                self.ser.write(b'7')
            if channel is 8:
                self.ser.write(b'8')
            if channel is 9 and self.daisy:
                self.ser.write(b'q')
            if channel is 10 and self.daisy:
                self.ser.write(b'w')
            if channel is 11 and self.daisy:
                self.ser.write(b'e')
            if channel is 12 and self.daisy:
                self.ser.write(b'r')
            if channel is 13 and self.daisy:
                self.ser.write(b't')
            if channel is 14 and self.daisy:
                self.ser.write(b'y')
            if channel is 15 and self.daisy:
                self.ser.write(b'u')
            if channel is 16 and self.daisy:
                self.ser.write(b'i')

    def find_port(self):
        """ Finds port that OpenBCI uses. Raise Error if none exist.

        :return: port name, if the right port exists
        """
        # find the serial port names depending on operating system
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith(
                'cygwin'):
            ports = glob.glob('/dev/ttyUSB*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.usbserial*')
        else:
            raise EnvironmentError(
                'Error finding ports on your operating system')

        # checks all ports for OpenBCI one
        openbci_port = ''
        for port in ports:
            try:
                s = serial.Serial(port=port, baudrate=self.baudrate, timeout=self.timeout)
                s.write(b'v')
                openbci_serial = self.openbci_id(s)
                s.close()
                if openbci_serial:
                    openbci_port = port
            except (OSError, serial.SerialException):
                pass

        if openbci_port == '':
            raise OSError('Cannot find OpenBCI port')
        else:
            return openbci_port


class OpenBCISample(object):
    """ Object encapulsating a single sample from the OpenBCI board. NB: dummy imp for plugin compatiblity """

    def __init__(self, packet_id, channel_data, aux_data):
        self.id = packet_id
        self.channel_data = channel_data
        self.aux_data = aux_data
        self.imp_data = []
