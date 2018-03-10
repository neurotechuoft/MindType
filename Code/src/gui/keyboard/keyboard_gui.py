import gui.keyboard.letter_keyboard

from PyQt5 import QtGui, QtCore, QtWidgets

# Sayan sucks; don't complain - yours truly Abdel and Scholar
# ^ Sayan is
from gui.keyboard.keyboards import Keyboards
from controller.MESSAGE import Message
from feature_flags.feature_flags import FeatureFlags


class KeyboardGUI(QtWidgets.QWidget):
    def __init__(self, main_controller, controllers, parent=None):
        super(KeyboardGUI, self).__init__(parent)

        self.CHAR_DISPLAY_PANEL_SHEET = "background-color: rgba(" \
                                             "255,255,255,220)"

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setAttribute(QtCore.Qt.WA_X11DoNotAcceptFocus)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # variables used for pausing
        self.main_controller = main_controller
        self.controllers = [main_controller] + controllers

        # Creating main panel which contains everything
        self.main_panel = QtWidgets.QVBoxLayout()
        self.main_panel.setContentsMargins(0, 0, 0, 0)

        # creating header panel which has pause/resume and text display
        self.header_panel = QtWidgets.QHBoxLayout()
        self.main_panel.addLayout(self.header_panel)

        # creating header panel buttons
        self.character_display_panel = QtWidgets.QLabel("Enter Text!")
        self.character_display_panel.setStyleSheet(
            self.CHAR_DISPLAY_PANEL_SHEET)
        self.end_button = QtWidgets.QPushButton("Resume")
        self.__PAUSED__ = True

        # setting button click listeners
        self.end_button.clicked.connect(self.pause_resume())

        # adding buttons to header panel
        self.header_panel.addWidget(self.character_display_panel)
        self.header_panel.addWidget(self.end_button)

        # adding keyboard gui to main panel
        # creating a button grid
        self.keyboards = Keyboards(self.character_display_panel)
        self.keyboards.keyboard_views.setCurrentIndex(0)

        self.main_panel.addLayout(self.keyboards.layout)

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
                self.keyboards.resume()
            else:
                button_pause_resume.setText("Resume")
                self.__PAUSED__ = True
                self.send_msg_to_controllers(Message.PAUSE)
                self.keyboards.pause()

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