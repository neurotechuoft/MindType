import argparse
import threading
import time
from controller.MESSAGE import Message

"""
    Helper functions to initialize board.
"""

def setup_parser():

    print ("------------main.py-------------")
    parser = argparse.ArgumentParser(description="OpenBCI 'user'")
    parser.add_argument('--board', default="cyton",
                        help="Choose between [cyton] and [ganglion] boards.")
    parser.add_argument('-l', '--list', action='store_true',
                        help="List available plugins.")
    parser.add_argument('-i', '--info', metavar='PLUGIN',
                        help="Show more information about a plugin.")
    parser.add_argument('-p', '--port',
                        help="For Cyton, port to connect to OpenBCI Dongle " +
                             "( ex /dev/ttyUSB0 or /dev/tty.usbserial-* ). For Ganglion, MAC address of the board. For both, AUTO to attempt auto-detection.")
    parser.set_defaults(port="AUTO")
    # baud rate is not currently used
    parser.add_argument('-b', '--baud', default=115200, type=int,
                        help="Baud rate (not currently used)")
    parser.add_argument('--no-filtering', dest='filtering',
                        action='store_false',
                        help="Disable notch filtering")
    parser.set_defaults(filtering=True)
    parser.add_argument('-d', '--daisy', dest='daisy',
                        action='store_true',
                        help="Force daisy mode (cyton board)")
    parser.add_argument('-x', '--aux', dest='aux',
                        action='store_true',
                        help="Enable accelerometer/AUX data (ganglion board)")
    # first argument: plugin name, then parameters for plugin
    parser.add_argument('-a', '--add', metavar=('PLUGIN', 'PARAM'),
                        action='append', nargs='+',
                        help="Select which plugins to activate and set parameters.")
    parser.add_argument('--log', dest='log', action='store_true',
                        help="Log program")
    parser.add_argument('--plugins-path', dest='plugins_path', nargs='+',
                        help="Additional path(s) to look for plugins")
    parser.set_defaults(daisy=False, log=False)

    return parser


def check_auto_port_selection(args):
    if "AUTO" == args.port.upper():
        print(
        "Will try do auto-detect board's port. Set it manually with '--port' if it goes wrong.")
        args.port = None
    else:
        print("Port: ", args.port)


def add_plugin(manager, plug_name, plug_args, plug_list, callback_list, board):
    # Try to find name
    plug = manager.getPluginByName(plug_name)
    if plug == None:
        # eg: if an import fail inside a plugin, yapsy skip it
        print (
        "Error: [ " + plug_name + " ] not found or could not be loaded. Check name and requirements.")
    else:
        print ("\nActivating [ " + plug_name + " ] plugin...")
        if not plug.plugin_object.pre_activate(plug_args,
                                               sample_rate=board.getSampleRate(),
                                               eeg_channels=board.getNbEEGChannels(),
                                               aux_channels=board.getNbAUXChannels(),
                                               imp_channels=board.getNbImpChannels()):
            print (
            "Error while activating [ " + plug_name + " ], check output for more info.")
        else:
            print ("Plugin [ " + plug_name + "] added to the list")
            plug_list.append(plug.plugin_object)
            callback_list.append(plug.plugin_object)


def print_logging_info(args, logging):
    if args.log:
        print ("Logging Enabled: " + str(args.log))
        logging.basicConfig(filename="OBCI.log",
                            format='%(asctime)s - %(levelname)s : %(message)s',
                            level=logging.DEBUG)
        logging.getLogger('yapsy').setLevel(logging.DEBUG)
        logging.info('---------LOG START-------------')
        logging.info(args)
    else:
        print ("main.py: Logging Disabled.")


def print_plugins_found(manager):
    print ("\n------------PLUGINS--------------")
    # Loop round the plugins and print their names.
    print ("Found plugins:")
    for plugin in manager.getAllPlugins():
        print ("[ " + plugin.name + " ]")
    print("\n")


def print_board_setup(board):
    """
    Print info about effective number of channels and sampling rate
    Args:
        board:

    Returns:

    """
    if board.daisy:
        print ("Force daisy mode:")
    else:
        print ("No daisy:")
        print (
        board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(),
        "AUX channels at", board.getSampleRate(), "Hz.")

def board_start(board, start_time, biosignal):
    lapse = -1
    board.setImpedance(False)

    boardThread = threading.Thread(target=board.start_board, args=(start_time, [biosignal, ], lapse))
    boardThread.daemon = True  # will stop on exit
    try:
        boardThread.start()
        print("Starting stream...")
    except:
        raise


def board_pause(board):
    board.stop()
    flush = True

    # We shouldn't be waiting to get messages every single time a message
    #  is sent to controller, because messages can be sent while the board is
    #  still running.
    # TODO: Move this block of code under Message.PAUSE
    poll_board_for_messages(board, flush)


def safe_exit(board, main_controller, biosignals=None):
    print("Attempting to safe-exit")
    if board.streaming:
        board.stop()

    print("Board stopped")

    for biosignal in biosignals:
        biosignal.exit()
    print("Biosignals exited")

    # cleanUp()
    board.disconnect()

    main_controller.send(Message.SAFE_TO_EXIT)

def poll_board_for_messages(board, flush):
    line = ''
    time.sleep(0.1)  # Wait to see if the board has anything to report
    # The Cyton nicely return incoming packets -- here supposedly messages -- whereas the Ganglion prints incoming ASCII message by itself
    if board.getBoardType() == "cyton":
        while board.ser_inWaiting():
            c = board.ser_read().decode('utf-8',
                                        errors='replace')  # we're supposed to get UTF8 text, but the board might behave otherwise
            line += c
            time.sleep(0.001)
            if (c == '\n') and not flush:
                print('%\t' + line[:-1])
                line = ''
    elif board.getBoardType() == "ganglion":
        while board.ser_inWaiting():
            board.waitForNotifications(0.001)
    if not flush:
        print(line)
    print("--Polling board for message: COMPLETE")
