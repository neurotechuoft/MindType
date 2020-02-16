# Keyboard Gui Class
# -------------------
import functools
import math
import random
import string
import time

from pykeyboard import PyKeyboard
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QTimer

from nlp.complete import autocomplete


class BaseKeyboard(QtWidgets.QWidget):

    __VIEW_ORDER__ = -1

    # constructor
    def __init__(self, keyboard_views, character_display_panel, interval):
        super().__init__()

        # Style sheets
        self.DEFAULT_STYLESHEET = "QPushButton {background-color: #444444; " \
                                  "color: white; font-size: 65px;}"
        self.ENTER_STYLESHEET = "QPushButton {background-color: #444444; " \
                                 "color: white; font-size: 63px;}"
        self.BKSP_STYLESHEET = "QPushButton {background-color: #444444; " \
                                "color: white; font-size: 40px;padding: 16px;}"
        self.SHIFT_STYLESHEET = "QPushButton {background-color: #444444; " \
                               "color: white; font-size: 57px;}"
        self.PREDICT_STYLESHEET = "QPushButton {background-color: #444444; " \
                                  "color: white; font-size: 50px;}"
        self.DARKEN_STYLESHEET = "QPushButton {background-color: #444444; " \
                                 "color: blue; font-size: 65px;}"

        self.keyboard_views = keyboard_views

        self.layout = QtWidgets.QVBoxLayout()

        self.character_display_panel = character_display_panel

        self.predict_buttons = []
        self.character_buttons = []

        # Top 3 Word Predictions
        self.predict_grid = QtWidgets.QGridLayout()
        self.predict_grid.setSpacing(0)

        self.make_predictions_widget(character_display_panel)

        # variables used for pausing
        self.flashing_interval = interval

        # attaching grid to main panel
        self.layout.addLayout(self.predict_grid)

        # variables used for flashing
        self.flash_timer_queue = []
        self.row_col_flash_order = []
        self.time_start = 0
        self.time_elapsed = 0

        self.current_text = ""

        self.keyboard_typer = PyKeyboard()

        self.setLayout(self.layout)

    @classmethod
    def start_context(cls, keyboard_views):
        keyboard_views.setCurrentIndex(cls.__VIEW_ORDER__)

    def make_predictions_widget(self, character_display_panel):
        for pred in range(3):
            button_name = ""
            button = QtWidgets.QPushButton(button_name)
            button.setStyleSheet(self.PREDICT_STYLESHEET)

            button.clicked.connect(functools.partial(self.print_prediction, button,
                                                     character_display_panel))

            self.predict_grid.addWidget(button, 0, pred)
            self.predict_buttons.append(button)

    def print_prediction(self, predict_btn, character_display_panel):

        prediction = predict_btn.text()

        # printing characters on same line
        print(prediction)
        display_panel_text = prediction + " "

        character_display_panel.setText(display_panel_text)

        self.reset_predictions()
        self.current_text = ""

    def update_predictions(self, word):
        pred_0, pred_1, pred_2 = autocomplete(word)

        self.predict_buttons[0].setText(pred_0)
        self.predict_buttons[1].setText(pred_1)
        self.predict_buttons[2].setText(pred_2)

        print("Top three: " + str(pred_0) + ", " + str(pred_1) + ", " + str(pred_2))

    def reset_predictions(self):
        for button in self.predict_buttons:
            button.setText("")

    def add_key_to_keyboard(self, key_grid,
                            button_name,
                            character_display_panel,
                            stylesheet,
                            row, col):
        button = QtWidgets.QPushButton(button_name)
        button.setStyleSheet(stylesheet)
        # adding button listener
        button.clicked.connect(functools.partial(self.press_key, button_name,
                                                 character_display_panel))
        key_grid.addWidget(button, row, col, alignment=QtCore.Qt.AlignTop)
        self.character_buttons.append(button)

    def press_key(self, char, character_display_panel):
        # printing characters on same line
        print(char)
        self.current_text += char

        # Punctuation indicates new word
        if char is " ":
            self.current_text = ""
            display_panel_text = " "
            self.reset_predictions()
        else:
            self.update_predictions(self.current_text)
            display_panel_text = self.current_text

        self.keyboard_typer.tap_key(char)

        character_display_panel.setText(display_panel_text)

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

        vector = self.get_row_and_col(row_col)
        print(vector)

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

    def calc_row_col(self, num, is_row):
        return num if is_row else 6 + num

    def get_row_and_col(self, row_col):
        num = row_col - 6 if row_col > 5 else row_col
        ret_id = "r" if row_col > 5 else "c"
        ret_id += str(num)

        return ret_id
