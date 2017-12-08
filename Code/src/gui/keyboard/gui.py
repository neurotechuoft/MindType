from PyQt4 import QtGui, QtCore

# Sayan sucks; don't complain - yours truly Abdel and Scholar
# ^ Sayan is

from Keyboard import Keyboard
from controller.MESSAGE import Message
from feature_flags.feature_flags import FeatureFlags


class GUI(QtGui.QDialog):
    def __init__(self, main_controller, controllers, parent=None):
        super(GUI, self).__init__(parent)

        self.CHAR_DISPLAY_PANEL_SHEET = "background-color: rgba(" \
                                             "255,255,255,220)"

        # variables used for pausing
        self.main_controller = main_controller
        self.controllers = [main_controller] + controllers
        self.interval = 100

        # Creating main panel which contains everything
        self.main_panel = QtGui.QVBoxLayout()
        self.main_panel.setContentsMargins(0, 0, 0, 0)

        # creating header panel which has pause/resume and text display
        self.header_panel = QtGui.QHBoxLayout()
        self.main_panel.addLayout(self.header_panel)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # creating header panel buttons
        self.character_display_panel = QtGui.QLabel("Enter Text!")
        self.character_display_panel.setStyleSheet(
            self.CHAR_DISPLAY_PANEL_SHEET)
        self.end_button = QtGui.QPushButton("Resume")
        self.__PAUSED__ = True

        # setting button click listeners
        self.end_button.clicked.connect(self.pause_resume())

        # adding buttons to header panel
        self.header_panel.addWidget(self.character_display_panel)
        self.header_panel.addWidget(self.end_button)

        # adding keyboard gui to main panel
        # creating a button grid
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)
        self.keyboard = Keyboard(self.main_panel, self.character_display_panel,
                                 self.interval)

        # setting layout to main_panel
        self.setLayout(self.main_panel)

    # signal functions (on click listeners)
    # -------------------------------------

    def pause_resume(self):

        def pause_resume_function():
            button_pause_resume = self.end_button
            if self.__PAUSED__:
                button_pause_resume.setText("Pause")
                self.__PAUSED__ = False
                self.send_msg_to_controllers(Message.START)
                self.keyboard.resume()
            else:
                button_pause_resume.setText("Resume")
                self.__PAUSED__ = True
                self.send_msg_to_controllers(Message.PAUSE)
                self.keyboard.pause()

        return pause_resume_function

    def closeEvent(self, event):
        if FeatureFlags.BOARD:
            safe_exit_confirmed = False

            self.send_msg_to_controllers(Message.EXIT)

            while not safe_exit_confirmed:
                if self.main_controller.search(Message.SAFE_TO_EXIT):
                    safe_exit_confirmed = True

            self.main_controller.send(Message.GUI_EXIT)

        event.accept()

    def send_msg_to_controllers(self, message):
        for controller in self.controllers:
            controller.send(message)
