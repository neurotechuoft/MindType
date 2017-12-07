from PyQt4 import QtGui, QtCore

# Sayan sucks; don't complain - yours truly Abdel and Scholar
# ^ Sayan is

from Keyboard import Keyboard
from controller.MESSAGE import Message


class GUI(QtGui.QDialog):
    def __init__(self, main_controller, controllers, parent=None):
        super(GUI, self).__init__(parent)

        self.char_display_panel_stylesheet = "background-color: rgba(" \
                "255,255,255,220)"

        # variables used for pausing
        self.main_controller = main_controller
        self.controllers = [main_controller] + controllers
        self.interval = 100

        # Creating main panel which contains everything
        self.main_panel = QtGui.QVBoxLayout()
        self.main_panel.setContentsMargins(0, 0, 0, 0)

        # creating header panel which has start, pause/resume and text display
        self.header_panel = QtGui.QHBoxLayout()
        self.main_panel.addLayout(self.header_panel)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # creating header panel buttons
        self.start_button = QtGui.QPushButton("Start")
        self.character_display_panel = QtGui.QLabel("Enter Text!")
        self.character_display_panel.setStyleSheet(
            self.char_display_panel_stylesheet)
        self.end_button = QtGui.QPushButton("Pause")

        # setting button click listeners
        self.start_button.clicked.connect(self.start())
        self.end_button.clicked.connect(self.pause_resume())

        # adding buttons to header panel
        self.header_panel.addWidget(self.character_display_panel)
        self.header_panel.addWidget(self.start_button)
        self.header_panel.addWidget(self.end_button)

        # adding keyboard gui to main panel
        # creating a button grid
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)
        self.keyboard = Keyboard(self.main_panel, self.character_display_panel, self.interval)

        # setting layout to main_panel
        self.setLayout(self.main_panel)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)



    # signal functions (on click listeners)
    # -------------------------------------
    def start(self):
        def start_function():
            # setting / resetting variables
            self.start_button.setDisabled(True)
            self.send_msg_to_controllers(Message.START)
            # print(self.controller)
            self.keyboard.start()

        return start_function

    def pause_resume(self):
        # print("Pause resume")

        def pause_resume_function():

            button_pause_resume = self.end_button
            # print("Before pause-resume")
            # print(self.controller)
            if button_pause_resume.text() == "Pause":
                button_pause_resume.setText("Resume")
                self.send_msg_to_controllers(Message.PAUSE)
                self.keyboard.pause()
            else:
                button_pause_resume.setText("Pause")
                self.send_msg_to_controllers(Message.START)
                self.keyboard.resume()
            # print("After pause-resume")
            # print(self.controller)

        return pause_resume_function

    def closeEvent(self, event):
        # safe_exit_confirmed = False
        #
        # self.send_msg_to_controllers(Message.EXIT)
        #
        # while not safe_exit_confirmed:
        #     if self.main_controller.search(Message.SAFE_TO_EXIT):
        #         safe_exit_confirmed = True
        #
        # self.main_controller.send(Message.GUI_EXIT)
        event.accept()

    def send_msg_to_controllers(self, message):
        for controller in self.controllers:
            controller.send(message)