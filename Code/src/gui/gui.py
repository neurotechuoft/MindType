import gui.keyboard.keyboard_gui
import gui.setup_gui
import json

from PyQt5 import QtGui, QtCore, QtWidgets

# Sayan sucks; don't complain - yours truly Abdel and Scholar
# ^ Sayan is
from gui.keyboard.keyboards import Keyboards
from controller.MESSAGE import Message
from feature_flags.feature_flags import FeatureFlags
from openbci_board.board_setup import safe_exit


class GUI(QtWidgets.QWidget):
    def __init__(self, board, biosignal, main_controller, controllers, parent=None):
        super(GUI, self).__init__(parent)

        self.main_controller = main_controller
        self.controllers = [main_controller] + controllers

        self.board = board
        self.biosignal = biosignal

        self.views = QtWidgets.QStackedWidget()

        self.keyboard_gui = gui.keyboard.keyboard_gui.KeyboardGUI(self.board,
                                                                    self.biosignal,
                                                                    self.main_controller,
                                                                    self.controllers)

        self.setup_gui = gui.setup_gui.SetupGUI()

        self.views.addWidget(self.setup_gui)
        self.views.addWidget(self.keyboard_gui)
        self.views.setCurrentIndex(1)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.views)

        self.setLayout(self.layout)

    def load_setup(self):
        with open("./../config.json") as setup_file:
            return json.loads(setup_file)

    def save_setup(self, setup):
        with open("./../config.json", "w") as setup_file:
            setup_file.write(json.dumps(setup))

    def confirm_initial_setup_finished(self):
        setup = self.load_setup()
        setup["initial_setup"] = True
        self.save_setup(setup)


    def closeEvent(self, event):
        if FeatureFlags.BOARD:
            safe_exit_confirmed = False

            self.send_msg_to_controllers(Message.EXIT)

            # while not safe_exit_confirmed:
            #     if self.main_controller.search(Message.SAFE_TO_EXIT):
            #         safe_exit_confirmed = True

            safe_exit(self.board, self.main_controller, [self.biosignal,])

            self.main_controller.send(Message.GUI_EXIT)

        event.accept()

    def send_msg_to_controllers(self, message):
        for controller in self.controllers:
            controller.send(message)