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
from gui.keyboard.letter_keyboard import LetterKeyboard
from nlp.complete import autocomplete


class NumberKeyboard(BaseKeyboard):

    __VIEW_ORDER__ = 1

    # constructor
    def __init__(self, keyboard_views, character_display_panel, interval):

        super().__init__(keyboard_views, character_display_panel, interval)

        # creating a button grid
        self.key_grid = self.make_numbers_widget(self.keyboard_views,
                                                 character_display_panel)

        self.layout.addLayout(self.key_grid)

    def make_numbers_widget(self, keyboard_views, character_display_panel):
        ret_num_grid = QtWidgets.QGridLayout()
        ret_num_grid.setSpacing(0)

        self.character_buttons = []

        for i in range(6):
            for j in range(6):
                num = i * 6 + j
                if num < 10:
                    self.add_key_to_keyboard(ret_num_grid, str(num), character_display_panel,
                                             i, j)
                elif num == 11:
                    button_name = 'a'

                    button = QtWidgets.QPushButton(button_name)
                    button.setStyleSheet(self.DEFAULT_STYLESHEET)
                    # adding button listener
                    button.clicked.connect(
                        functools.partial(LetterKeyboard.start_context,
                                          keyboard_views))
                    ret_num_grid.addWidget(button, i, j, alignment=QtCore.Qt.AlignTop)
                    self.character_buttons.append(button)

        return ret_num_grid
