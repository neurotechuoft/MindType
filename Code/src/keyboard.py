import functools
import random
import sys

import time

import math
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer


# Sayan sucks; don't complain
class MindType(QtGui.QWidget):
    def __init__(self):
        super(MindType, self).__init__()

        # variables used for pausing
        self.paused = False
        self.interval = 100

        # Creating main panel which contains everything
        self.main_panel = QtGui.QVBoxLayout()
        self.main_panel.setContentsMargins(0, 0, 0, 0)

        # creating header panel which has start, pause/resume and text display
        self.header_panel = QtGui.QHBoxLayout()
        self.main_panel.addLayout(self.header_panel)

        # creating header panel buttons
        self.character_display_panel = QtGui.QLabel("Enter Text!")
        self.start_button = QtGui.QPushButton("Start")
        self.end_button = QtGui.QPushButton("Pause")

        # setting button click listeners
        self.start_button.clicked.connect(self.start())
        self.end_button.clicked.connect(self.pause_resume())

        # adding buttons to header panel
        self.header_panel.addWidget(self.character_display_panel)
        self.header_panel.addWidget(self.start_button)
        self.header_panel.addWidget(self.end_button)

        # adding keyboard gui to main panel
        self.keyboard = Keyboard(self.main_panel, self.character_display_panel, self.interval)

        # setting layout to main_panel
        self.setLayout(self.main_panel)

    # signal functions (on click listeners)
    # -------------------------------------
    def start(self):
        def start_function():
            # setting / resetting variables
            self.start_button.setDisabled(True)
            self.paused = False
            self.keyboard.start()

        return start_function

    def pause_resume(self):
        def pause_resume_function():
            button_pause_resume = self.end_button
            if button_pause_resume.text() == "Pause":
                button_pause_resume.setText("Resume")
                self.is_paused = True
                self.keyboard.pause()

            else:
                button_pause_resume.setText("Pause")
                self.is_paused = False
                self.keyboard.resume()

        return pause_resume_function


# Keyboard Gui Class
# -------------------
class Keyboard:
    # constructor
    def __init__(self, main_panel, character_display_panel, interval):

        # variables used for pausing
        self.flashing_interval = interval

        # creating a button grid
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)

        self.character_buttons = []
        # adding keyboard buttons to the grid)
        for row in range(6):
            for col in range(6):
                character_number = (row * 6) + col
                # a-z buttons
                if character_number < 26:
                    button_name = chr(ord('a') + character_number)
                # 0-9 buttons
                else:
                    button_name = str(character_number - 26)

                button = QtGui.QPushButton(button_name)
                button.setStyleSheet("QPushButton {background-color: black; color: white; font-size: 65px;}")

                # adding button listener
                button.clicked.connect(functools.partial(self.print_char, button_name, character_display_panel))
                self.grid.addWidget(button, row, col)
                self.character_buttons.append(button)

        # attaching grid to main panel
        main_panel.addLayout(self.grid)

        # variables used for flashing
        self.flash_timer_queue = []
        self.row_col_flash_order = []
        self.time_start = 0
        self.time_elapsed = 0

    def print_char(self, name, character_display_panel):
        # printing characters on same line
        print(name),
        if character_display_panel.text() == "Enter Text!":
            character_display_panel.setText(name)
        else:
            character_display_panel.setText(character_display_panel.text() + name)

    def start(self):
        self.row_col_flash_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.setup_flash()
        self.flash()

    def pause(self):
        for timer in self.flash_timer_queue:
            timer.stop()
            self.time_elapsed = (time.time() - self.time_start)
        for button in self.character_buttons:
            button.setStyleSheet("QPushButton {background-color: black; color: white; font-size: 65px;}")

        print self.time_elapsed

    def resume(self):
        # Resuming
        resume_index = int(math.ceil((self.time_elapsed * 1000) / (self.flashing_interval * 2)))
        self.row_col_flash_order = self.row_col_flash_order[resume_index:len(self.row_col_flash_order)]
        self.setup_flash()
        self.flash()

    # method to create a random (row/col) order flashing queue
    def setup_flash(self):
        # setting flashing variables
        self.flash_timer_queue = []
        random.shuffle(self.row_col_flash_order)
        self.time_start = time.time()

        #
        for row_col in self.row_col_flash_order:
            # creating darken row/col instructions for specific row
            timer_darken = QTimer()
            timer_darken.setSingleShot(True)
            timer_darken.timeout.connect(functools.partial(self.change_color, row_col, "darken"))
            # creating lighten row/col instructions for specific row
            timer_lighten = QTimer()
            timer_lighten.setSingleShot(True)
            timer_lighten.timeout.connect(functools.partial(self.change_color, row_col, "lighten"))
            # adding the flash row/col instruction to queue
            self.flash_timer_queue.append(timer_darken)
            self.flash_timer_queue.append(timer_lighten)

        # adding enable start button instruction to Queue
        # TODO - create an instruction class/method
        button_timer = QTimer()
        button_timer.setSingleShot(True)
        button_timer.timeout.connect(functools.partial(self.run_again))
        self.flash_timer_queue.append(button_timer)

    def flash(self):
        counter = 0
        self.time_start = time.time()
        for instruction in self.flash_timer_queue:
            instruction.start(counter)
            counter += self.flashing_interval

            # function that lightens/darken a row/col

    def change_color(self, row_col, color):
        keyboard_buttons = self.character_buttons
        is_row = False
        if row_col > 5:
            row_col = row_col - 6
            is_row = True

        for index in range(6):
            # displaying rows
            if is_row:
                keyboard_button = keyboard_buttons[index + (row_col * 6)]
            # displaying col
            else:
                keyboard_button = keyboard_buttons[(index * 6) + row_col]

            if color == "lighten":
                keyboard_button.setStyleSheet("QPushButton {background-color: black; color: white; font-size: 65px;}")
            elif color == "darken":
                keyboard_button.setStyleSheet("QPushButton {background-color: black; color: blue; font-size: 65px;}")

    # pause between each character flashing
    def run_again(self):
        QTimer.singleShot(self.flashing_interval * 3, functools.partial(self.start))


# main method
# -----------
if __name__ == '__main__':
    # Running gui
    app = QtGui.QApplication(sys.argv)
    mindType = MindType()
    mindType.resize(550, 550)
    mindType.show()
    sys.exit(app.exec_())
