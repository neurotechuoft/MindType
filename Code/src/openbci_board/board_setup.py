import argparse

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
    if board.daisy:
        print ("Force daisy mode:")
    else:
        print ("No daisy:")
        print (
        board.getNbEEGChannels(), "EEG channels and", board.getNbAUXChannels(),
        "AUX channels at", board.getSampleRate(), "Hz.")