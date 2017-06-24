import functools
import random
import sys

import time

import math
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer


# Keyboard Gui Class
# -------------------
class Keyboard(QtGui.QWidget):
    v_box = QtGui.QVBoxLayout()
    h_box = QtGui.QHBoxLayout()
    grid = QtGui.QGridLayout()

    # constructor
    def __init__(self):
        super(Keyboard, self).__init__()

        # creating a grid of buttons, setting margins and spacing (adding to v_box)
        Keyboard.grid.setSpacing(0)
        Keyboard.v_box.setContentsMargins(0, 0, 0, 0)

        # adding top bar for keyboard (adding to h_box)
        self.character_display_panel = QtGui.QLabel("Enter Text!")
        self.start_button = QtGui.QPushButton("Start")
        self.end_button = QtGui.QPushButton("Pause")

        self.start_button.clicked.connect(start(self))
        self.end_button.clicked.connect(pause_resume(self))

        # variables used for pausing
        self.flash_timer_queue = []
        self.row_col_flash_order = []
        self.time_start = 0
        self.time_elapsed = 0
        self.flashing_interval = 250
        self.paused = False

        Keyboard.h_box.addWidget(self.character_display_panel)
        Keyboard.h_box.addWidget(self.start_button)
        Keyboard.h_box.addWidget(self.end_button)

        self.character_buttons = []
        # adding keyboard keys (adding to grid)
        for i in range(6):
            for j in range(6):
                character_number = (i * 6) + j

                if character_number < 26:
                    button_name = chr(ord('a') + character_number)
                else:
                    button_name = str(character_number - 26)
                # button_name = chr(ord('a') + (i * 6) + j)
                button = QtGui.QPushButton(button_name)
                button.setStyleSheet("QPushButton {background-color: black; color: white; font-size: 65px;}")
                # adding buttons to grid and creating a listener (signals in python?)
                button.clicked.connect(print_char(button_name, self))
                Keyboard.grid.addWidget(button, i, j)
                self.character_buttons.append(button)

        # attaching grid and h_box to the v_box
        Keyboard.v_box.addLayout(Keyboard.h_box)
        Keyboard.v_box.addLayout(Keyboard.grid)
        # setting the layout of of Keyboard to v_box
        self.setLayout(Keyboard.v_box)


# signal functions (on click listeners)
# -------------------------------------
def start(keyboard):
    def start_function():
        # setting / resetting variables
        keyboard.start_button.setDisabled(True)
        keyboard.row_col_flash_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        keyboard.paused = False
        setup_flash(keyboard)

        # call flashing function
        flash(keyboard)

    return start_function


def pause_resume(keyboard):
    def pause_resume_function():
        button_pause_resume = keyboard.end_button
        if button_pause_resume.text() == "Pause":
            button_pause_resume.setText("Resume")
            keyboard.is_paused = True
            for timer in keyboard.flash_timer_queue:
                timer.stop()
            keyboard.time_elapsed = (time.time() - keyboard.time_start)
            for button in keyboard.character_buttons:
                button.setStyleSheet("QPushButton {background-color: black; color: white; font-size: 65px;}")

            print keyboard.time_elapsed
        else:
            button_pause_resume.setText("Pause")
            keyboard.is_paused = False
            # Resuming
            resume_index = int(math.ceil((keyboard.time_elapsed * 1000) / (keyboard.flashing_interval * 2)))
            keyboard.row_col_flash_order = keyboard.row_col_flash_order[
                                           resume_index:len(keyboard.row_col_flash_order)]
            setup_flash(keyboard)
            flash(keyboard)

    return pause_resume_function


def print_char(name, keyboard):
    def print_char_function():
        # printing characters on same line
        print(name),
        display_panel = keyboard.character_display_panel
        if display_panel.text() == "Enter Text!":
            display_panel.setText(name)
        else:
            display_panel.setText(keyboard.character_display_panel.text() + name)

    return print_char_function  # (ButtonBlock --> extends QWidget)


# helper Signal functions
# ------------------------
# method to create a random (row/col) order flashing queue
def setup_flash(keyboard):
    keyboard.flash_timer_queue = []
    random.shuffle(keyboard.row_col_flash_order)
    keyboard.time_start = time.time()
    for row_col in keyboard.row_col_flash_order:
        # creating darken row/col instructions for specific row
        timer_darken = QTimer()
        timer_darken.setSingleShot(True)
        timer_darken.timeout.connect(functools.partial(change_color, keyboard, row_col, "darken"))
        # creating lighten row/col instructions for specific row
        timer_lighten = QTimer()
        timer_lighten.setSingleShot(True)
        timer_lighten.timeout.connect(functools.partial(change_color, keyboard, row_col, "lighten"))
        # adding the flash row/col instruction to queue
        keyboard.flash_timer_queue.append(timer_darken)
        keyboard.flash_timer_queue.append(timer_lighten)

    # adding enable start button instruction to Queue
    # TODO - create an instruction class/method
    button_timer = QTimer()
    button_timer.setSingleShot(True)
    button_timer.timeout.connect(functools.partial(run_again, keyboard))
    keyboard.flash_timer_queue.append(button_timer)


def flash(keyboard):
    counter = 0
    keyboard.time_start = time.time()
    for instruction in keyboard.flash_timer_queue:
        instruction.start(counter)
        counter += keyboard.flashing_interval


# function that lightens/darken a row/col
def change_color(keyboard, row_col, color):
    keyboard_buttons = keyboard.character_buttons
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


def run_again(keyboard):
    keyboard.start_button.setEnabled(True)
    keyboard.start_button.click()
    keyboard.start_button.setEnabled(False)


# main method
# -----------
if __name__ == '__main__':
    # Running gui
    app = QtGui.QApplication(sys.argv)
    keyboard_gui = Keyboard()
    keyboard_gui.resize(550, 550)
    keyboard_gui.show()
    sys.exit(app.exec_())
