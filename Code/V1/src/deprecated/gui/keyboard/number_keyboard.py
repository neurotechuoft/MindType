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

import gui.keyboard.base_keyboard
import gui.keyboard.letter_keyboard
from nlp.complete import autocomplete


class NumberKeyboard(gui.keyboard.base_keyboard.BaseKeyboard):

    __VIEW_ORDER__ = 1

    # constructor
    def __init__(self, keyboard_views, character_display_panel, interval):

        super().__init__(keyboard_views, character_display_panel, interval)

        self.NUMBER_STYLESHEET = "QPushButton {background-color: #444444; " \
                                  "color: white; font-size: 100px;}"

        # creating a button grid
        self.key_grid = self.make_numbers_widget(self.keyboard_views,
                                                 character_display_panel)

        self.layout.addLayout(self.key_grid)

    def make_numbers_widget(self, keyboard_views, character_display_panel):
        ret_num_grid = QtWidgets.QGridLayout()
        ret_num_grid.setSpacing(0)

        self.character_buttons = []

        for i in range(4):
            for j in range(4):
                num = i * 4 + j
                if num < 10:
                    self.add_key_to_keyboard(ret_num_grid, str(num), character_display_panel, self.NUMBER_STYLESHEET,
                                             i, j)
                elif num == 11:
                    button_name = 'a'

                    button = QtWidgets.QPushButton(button_name)
                    button.setStyleSheet(self.NUMBER_STYLESHEET)
                    # adding button listener
                    button.clicked.connect(
                        functools.partial(gui.keyboard.letter_keyboard.LetterKeyboard.start_context,
                                          keyboard_views))
                    ret_num_grid.addWidget(button, i, j, alignment=QtCore.Qt.AlignTop)
                    self.character_buttons.append(button)

        return ret_num_grid
