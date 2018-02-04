# Keyboard Gui Class
# -------------------
import functools
import math
import random
import time

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QTimer


class Keyboard:
    # constructor
    def __init__(self, main_panel, character_display_panel, interval):
        # Style sheets
        self.DEFAULT_STYLESHEET = "QPushButton {background-color: #444444; " \
                                     "color: white; font-size: 65px;}"
        self.PREDICT_STYLESHEET = "QPushButton {background-color: #444444; " \
                                  "color: white; font-size: 50px;}"
        self.DARKEN_STYLESHEET = "QPushButton {background-color: #444444; " \
                                 "color: blue; font-size: 65px;}"

        # creating a button grid
        self.key_grid = QtWidgets.QGridLayout()
        self.key_grid.setSpacing(0)

        # Top 3 Word Predictions
        self.predict_grid = QtWidgets.QGridLayout()
        self.predict_grid.setSpacing(0)

        self.predict_buttons = []
        self.character_buttons = []

        self.make_predictions_widget()

        # variables used for pausing
        self.flashing_interval = interval

        # adding keyboard buttons to the grid)


        for row in range(6):
            for col in range(6):
                # button_name = ""
                character_number = (row * 6) + col
                # a-z buttons
                if character_number < 26:
                    button_name = chr(ord('a') + character_number)
                    self.add_key_to_keyboard(button_name,
                                             character_display_panel,
                                             row, col)

                elif character_number is 26:
                    button_name = "0"

                    button = QtWidgets.QPushButton(button_name)
                    button.setStyleSheet(self.DEFAULT_STYLESHEET)
                    # adding button listener
                    button.clicked.connect(
                        functools.partial(self.start_number_context,
                                          character_display_panel))
                    self.key_grid.addWidget(button, row, col, alignment = QtCore.Qt.AlignTop)
                    self.character_buttons.append(button)

                else:
                    pass

                # # 0-9 buttons
                # else:
                #     button_name = str(character_number - 26)
                #     self.add_key_to_keyboard(button_name,
                #                          character_display_panel,
                #                          row, col)



        # attaching grid to main panel
        main_panel.addLayout(self.predict_grid)
        main_panel.addLayout(self.key_grid)

        # variables used for flashing
        self.flash_timer_queue = []
        self.row_col_flash_order = []
        self.time_start = 0
        self.time_elapsed = 0

    def make_predictions_widget(self):
        for pred in range(3):
            button_name = "pred" + str(pred)
            button = QtWidgets.QPushButton(button_name)
            button.setStyleSheet(self.PREDICT_STYLESHEET)

            self.predict_grid.addWidget(button, 0, pred)
            self.predict_buttons.append(button)

    def add_key_to_keyboard(self,
                            button_name,
                            character_display_panel,
                            row, col):
        button = QtWidgets.QPushButton(button_name)
        button.setStyleSheet(self.DEFAULT_STYLESHEET)
        # adding button listener
        button.clicked.connect(functools.partial(self.print_char, button_name,
                                                 character_display_panel))
        self.key_grid.addWidget(button, row, col, alignment = QtCore.Qt.AlignTop)
        self.character_buttons.append(button)

    def print_char(self, name, character_display_panel):
        # printing characters on same line
        print(name),
        if character_display_panel.text() == "Enter Text!":
            character_display_panel.setText(name)
        else:
            character_display_panel.setText(character_display_panel.text() + name)

    def start_number_context(self, character_display_panel):
        num = 0

        for btn in self.character_buttons:
            btn.deleteLater()

        self.character_buttons = []

        for i in range(6):
            for j in range(6):
                num = i * 6 + j
                if num < 10:
                    self.add_key_to_keyboard(str(num), character_display_panel,
                                             i, j)


    def start(self):
        self.row_col_flash_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.setup_flash()
        self.flash()

    def pause(self):
        for timer in self.flash_timer_queue:
            timer.stop()
            self.time_elapsed = (time.time() - self.time_start)
        for button in self.character_buttons:
            button.setStyleSheet(self.DEFAULT_STYLESHEET)

        print(self.time_elapsed)

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

            btn_id = index + (row_col * 6) if is_row else (index * 6) + row_col
            stylesheet = self.DEFAULT_STYLESHEET if color is "lighten" \
                else self.DARKEN_STYLESHEET

            if btn_id < len(keyboard_buttons):
                keyboard_button = keyboard_buttons[btn_id]
                keyboard_button.setStyleSheet(stylesheet)


    # pause between each character flashing
    def run_again(self):
        QTimer.singleShot(self.flashing_interval * 3, functools.partial(self.start))
