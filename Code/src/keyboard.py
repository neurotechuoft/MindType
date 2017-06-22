import functools
import random
import sys

from PyQt4 import QtGui
from PyQt4.QtCore import QTimer

is_paused = False
current_index = 0


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
        self.start_button = QtGui.QPushButton("Start / Next letter")
        self.end_button = QtGui.QPushButton("Pause")

        self.start_button.clicked.connect(start(self))
        self.end_button.clicked.connect(pause_resume(self))

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
                label = QtGui.QPushButton(button_name)
                label.setStyleSheet("QLabel {background-color: black; color: white; font-size: 65px;}")
                # adding buttons to grid and creating a listener (signals in python?)
                label.clicked.connect(print_char(button_name, self))
                Keyboard.grid.addWidget(label, i, j)
                self.character_buttons.append(label)

        # attaching grid and h_box to the v_box
        Keyboard.v_box.addLayout(Keyboard.h_box)
        Keyboard.v_box.addLayout(Keyboard.grid)
        # setting the layout of of Keyboard to v_box
        self.setLayout(Keyboard.v_box)


# signal functions (on click listeners)
# -------------------------------------
def start(keyboard):
    def start_function():
        button_start = keyboard.start_button
        # button_start.setDisabled(True)
        run_flash(keyboard)

    return start_function


def pause_resume(keyboard):
    def pause_resume_function():
        global is_paused
        button_pause_resume = keyboard.end_button
        if button_pause_resume.text() == "Pause":
            button_pause_resume.setText("Resume")
            is_paused = True
        else:
            button_pause_resume.setText("Pause")
            is_paused = False
            # cont.

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
# driver method for flash function
def run_flash(keyboard):
    global current_index, is_paused, q_timer

    row_col_visited = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    random.shuffle(row_col_visited)

    for index in range(12):
        counter = 300 * (index + 1)
        row_col = row_col_visited[index]
        QTimer.singleShot(counter, functools.partial(flash, keyboard, row_col))


# setting time intervals for flashing
def flash(keyboard, row_col):
    if is_paused:
        QTimer.stop()
    else:
        QTimer.singleShot(0, functools.partial(change_color, keyboard, row_col, "dark"))
        QTimer.singleShot(200, functools.partial(change_color, keyboard, row_col, "light"))


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

        if color == "light":
            keyboard_button.setStyleSheet("QPushButton {background-color: black; color: white; font-size: 65px;}")
        else:
            keyboard_button.setStyleSheet("QPushButton {background-color: black; color: blue; font-size: 65px;}")


def init_flash(block):
    for x in range(12):
        flash(block, x)


# main method
# -----------
if __name__ == '__main__':
    # Running gui
    app = QtGui.QApplication(sys.argv)
    buttonBlock = Keyboard()
    init_flash(buttonBlock)
    buttonBlock.resize(550, 550)
    buttonBlock.show()
    sys.exit(app.exec_())
