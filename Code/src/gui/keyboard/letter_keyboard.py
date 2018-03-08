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

from gui.keyboard.base_keyboard import BaseKeyboard
from gui.keyboard.number_keyboard import NumberKeyboard
from nlp.complete import autocomplete


class LetterKeyboard(BaseKeyboard):

    __VIEW_ORDER__ = 0

    # constructor
    def __init__(self, keyboard_views, character_display_panel, interval):

        super().__init__(keyboard_views, character_display_panel, interval)

        # creating a button grid
        self.key_grid = self.make_letters_widget(self.keyboard_views,
                                                 character_display_panel)

        self.layout.addLayout(self.key_grid)

    def make_letters_widget(self, keyboard_views, character_display_panel):
        ret_key_grid = QtWidgets.QGridLayout()
        ret_key_grid.setSpacing(0)

        for row in range(6):
            for col in range(6):
                # button_name = ""
                character_number = (row * 6) + col
                # a-z buttons
                if character_number < 26:
                    button_name = chr(ord('a') + character_number)
                    self.add_key_to_keyboard(ret_key_grid,
                                             button_name,
                                             character_display_panel,
                                             row, col)

                elif character_number == 26:
                    button_name = "0"

                    button = QtWidgets.QPushButton(button_name)
                    button.setStyleSheet(self.DEFAULT_STYLESHEET)
                    # adding button listener
                    button.clicked.connect(
                        functools.partial(NumberKeyboard.start_context,
                                          keyboard_views))
                    ret_key_grid.addWidget(button, row, col, alignment=QtCore.Qt.AlignTop)
                    self.character_buttons.append(button)

                elif character_number == 27:
                    button_name = "space"
                    button = QtWidgets.QPushButton(button_name)
                    button.setStyleSheet(self.DEFAULT_STYLESHEET)
                    button.clicked.connect(functools.partial(self.press_key, " ",
                                                             character_display_panel))
                    ret_key_grid.addWidget(button, row, col, alignment=QtCore.Qt.AlignTop)
                    self.character_buttons.append(button)

                else:
                    pass

        return ret_key_grid
