#!/usr/bin/env python2.7
import atexit
import logging
import sys
import threading
import time
from PyQt4 import QtGui

from biosignals.print_biosignal import PrintBiosignal
from biosignals.tagger import Tagger
from controller.MESSAGE import Message
from controller.controller import Controller
from controller.processor import Processor
from feature_flags.feature_flags import FeatureFlags
from gui.dev_tools import DevTools
from gui.keyboard.gui import GUI
from openbci_board.board_setup import setup_parser, check_auto_port_selection, \
    add_plugin, print_logging_info, print_plugins_found, print_board_setup

logging.basicConfig(level=logging.ERROR)

from yapsy.PluginManager import PluginManager

def make_gui(main_controller, controllers):
    app = QtGui.QApplication(sys.argv)
    main_scr = None
    if FeatureFlags.GUI:
        main_scr = GUI(main_controller, controllers)
    if FeatureFlags.DEV_TOOLS:
        main_scr = DevTools(main_controller, controllers)
    if main_scr is not None:
        main_scr.resize(500, 100)
        main_scr.show()
    sys.exit(app.exec_())


def safe_exit(board, main_controller, biosignals=None):
    print("Attempting to safe-exit")
    if board.streaming:
        board.stop()

    print("Board stopped")

    for biosignal in biosignals:
        biosignal.exit()
    print("Biosignals exited")

    cleanUp()

    main_controller.send(Message.SAFE_TO_EXIT)


def board_action(board, controller, pub_sub_fct, biosignal=None):
    """
    Reads message from controller, and executes required action on the board.
        Examples include starting, pausing, and exiting the board.

    Args:
        board:
        controller:
        pub_sub_fct:
        biosignal:

    Returns:

    """

    message = controller.read()
    print("Incoming message: " + str(message))

    flush = False
    recognized = False  # current command is recognized or fot
    lapse = -1

    if message is Message.START:
        board.setImpedance(False)
        # TODO: should we also add 'and not  baord.streaming'
        if pub_sub_fct is not None:
            # start streaming in a separate thread so we could always send commands in here
            boardThread = threading.Thread(
                target=board.start_streaming, args=(pub_sub_fct, lapse,
                                                    [biosignal,]))
            boardThread.daemon = True  # will stop on exit
            try:
                boardThread.start()
                print("Starting stream...")
            except:
                raise
        else:
            print ("No function loaded")
        recognized = True

    elif message is Message.PAUSE:
        board.stop()
        recognized = True
        flush = True

        # We shouldn't be waiting to get messages every single time a message
        #  is sent to controller, because messages can be sent while the board is
        #  still running.
        # TODO: Move this block of code under Message.PAUSE
        poll_board_for_messages(board, flush)
    elif message is Message.EXIT:
        controller.send(Message.EXIT)
        return

    if recognized == False:
        print("Command not recognized...")


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


def execute_board(board, controller, fun, biosignal, processor):
    print ("--------------INFO---------------")
    print ("User serial interface enabled...\n\
View command map at http://docs.openbci.com.\n\
Type /start to run (/startimp for impedance \n\
checking, if supported) -- and /stop\n\
before issuing new commands afterwards.\n\
Type /exit to exit. \n\
Board outputs are automatically printed as: \n\
%  <tab>  message\n\
$$$ signals end of message")
    print("\n-------------BEGIN---------------")
    # # Init board state
    # # s: stop board streaming; v: soft reset of the 32-bit board (no effect with 8bit board)
    # s = 'sv'
    # # Tell the board to enable or not daisy module
    # if board.daisy:
    #     s = s + 'C'
    # else:
    #     s = s + 'c'
    # # d: Channels settings back to default
    # s = s + 'd'

    while True:
        if controller.peek() is Message.EXIT:
            safe_exit(board, controller, [biosignal, ])
            print("Execute board exiting")
            return

        if controller.peek() is not None:
            board_action(board, controller, fun, biosignal)
            if FeatureFlags.COMMAND_LINE:
                user_control([controller,
                              biosignal.controller,
                              processor.controller]) # don't need this



def user_control(controllers):
    s = get_user_input()

    message = parse_user_input(s)

    if message is not None:
        send_msg_to_controllers(controllers, message)


def get_user_input():
    # Take user input
    if sys.hexversion > 0x03000000:
        s = input('--> ')
    else:
        s = raw_input('--> ')
    return s


def parse_user_input(s):
    if s is None:
        return None
    elif "/start" in s:
        return Message.START
    elif "/stop" in s:
        return Message.PAUSE
    elif "/exit" in s:
        return Message.EXIT
    else: return s


def send_msg_to_controllers(controllers, message):
    for controller in controllers:
        controller.send(message)


def run_processor(processor):
    message = Message.IDLE

    while message is not Message.EXIT:
        # print("Processing...")
        message = processor.process()
    print("Processor exited")


if __name__ == '__main__':
    # VARIABLES-----------------------------------------------------------------
    manager = PluginManager() # Load the plugins from the plugin directory.
    main_controller = Controller()
    if FeatureFlags.DEV_TOOLS:
        biosignal = Tagger("./test_results/data.csv")
    else:
        biosignal = PrintBiosignal()
    processor = Processor([biosignal])

    # SET UP GUI----------------------------------------------------------------
    if not FeatureFlags.COMMAND_LINE:
        gui_thread = threading.Thread(target=make_gui,
                                      args=[main_controller,
                                            [biosignal.controller,
                                             processor.controller]])
        gui_thread.daemon = True
        gui_thread.start()

    # SET UP BOARD--------------------------------------------------------------
    parser = setup_parser()
    args = parser.parse_args()

    if not(args.add):
        print ("WARNING: no plugin selected, you will only be able to communicate with the board. You should select at least one plugin with '--add [plugin_name]'. Use '--list' to show available plugins or '--info [plugin_name]' to get more information.")

    if args.board == "cyton":
        print ("Board type: OpenBCI Cyton (v3 API)")
        import openbci_board.open_bci_v3 as bci
    elif args.board == "ganglion":
        print ("Board type: OpenBCI Ganglion")
        import openbci_board.open_bci_ganglion as bci
    else:
        raise ValueError('Board type %r was not recognized. Known are 3 and 4' % args.board)

    # Check AUTO port selection, a "None" parameter for the board API
    check_auto_port_selection(args)

    # Collect plugins
    plugins_paths = ["plugins"]
    if args.plugins_path:
        plugins_paths += args.plugins_path
    manager.setPluginPlaces(plugins_paths)
    manager.collectPlugins()

    print ("\n------------SETTINGS-------------")
    print ("Notch filtering:" + str(args.filtering))

    # Logging
    print_logging_info(args, logging)

    print ("\n-------INSTANTIATING BOARD-------")
    board = bci.OpenBCIBoard(port=args.port,
                             daisy=args.daisy,
                             filter_data=args.filtering,
                             scaled_output=True,
                             log=args.log,
                             aux=args.aux)

    print_board_setup(board)
    print_plugins_found(manager)

    # Fetch plugins, try to activate them, add to the list if OK
    plug_list = []
    callback_list = []
    if args.add:
        for plug_candidate in args.add:
            # first value: plugin name, then optional arguments
            plug_name = plug_candidate[0]
            plug_args = plug_candidate[1:]
            add_plugin(manager, plug_name, plug_args, plug_list, callback_list,
                       board)

    if len(plug_list) == 0:
        fun = None
        print("No function loaded!")
    else:
        fun = callback_list

    def cleanUp():
        board.disconnect()
        print ("Deactivating Plugins...")
        for plug in plug_list:
            plug.deactivate()
        print ("User.py exiting...")

    atexit.register(cleanUp)

    # EXECUTE APPLICATION-------------------------------------------------------
    process_thread = threading.Thread(target=run_processor, args=(processor,))
    process_thread.start()

    execute_board(board, main_controller, fun, biosignal, processor)

    # FINISH EXIT PROCESS
    ready_for_exit = False
    while not ready_for_exit:
        if main_controller.search(Message.GUI_EXIT):
            ready_for_exit = True

    print("Final goodbye!")
