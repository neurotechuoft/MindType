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
import gui.keyboard.number_keyboard
from nlp.complete import autocomplete


class LetterKeyboard(gui.keyboard.base_keyboard.BaseKeyboard):

    __VIEW_ORDER__ = 0

    # constructor
    def __init__(self, keyboard_views, character_display_panel, interval):

        super().__init__(keyboard_views, character_display_panel, interval)

        # creating a button grid
        self.key_grid = self.make_letters_widget(self.keyboard_views,
                                                 character_display_panel)

        # Context switching grid
        self.context_switch_grid = self.make_context_switch_grid(keyboard_views)

        self.layout.addLayout(self.key_grid)
        self.layout.addLayout(self.context_switch_grid)

    def make_letters_widget(self, keyboard_views, character_display_panel):
        ret_key_grid = QtWidgets.QGridLayout()
        ret_key_grid.setSpacing(0)

        for row in range(6):
            for col in range(6):
                # button_name = ""
                character_number = (row * 6) + col
                # a-x buttons
                if character_number < 24:
                    button_name = chr(ord('a') + character_number)
                    self.add_key_to_keyboard(ret_key_grid,
                                             button_name,
                                             character_display_panel,
                                             row, col)
                # y, z
                elif character_number == 26 or character_number == 27:
                    button_name = chr(ord('a') + character_number - 2)
                    self.add_key_to_keyboard(ret_key_grid,
                                             button_name,
                                             character_display_panel,
                                             row, col)
                # Shift
                elif character_number == 28:
                    button_name = u"\U0001F839"
                    button = QtWidgets.QPushButton(button_name)
                    button.setStyleSheet(self.SHIFT_STYLESHEET)
                    # adding button listener
                    # button.clicked.connect(
                    #     functools.partial(gui.keyboard.number_keyboard.NumberKeyboard.start_context,
                    #                       keyboard_views))
                    ret_key_grid.addWidget(button, row, col, 1, 2, alignment=QtCore.Qt.AlignTop)
                    self.character_buttons.append(button)

                # Space
                elif character_number == 24:
                    button_name = "_____"
                    button = QtWidgets.QPushButton(button_name)
                    button.setStyleSheet(self.DEFAULT_STYLESHEET)
                    button.clicked.connect(functools.partial(self.press_key, " ",
                                                             character_display_panel))
                    ret_key_grid.addWidget(button, row, col, 1, 2, alignment=QtCore.Qt.AlignTop)
                    self.character_buttons.append(button)

                else:
                    pass

        return ret_key_grid

    def make_context_switch_grid(self, keyboard_views):
        ret_context_switch_grid = QtWidgets.QGridLayout()
        ret_context_switch_grid.setSpacing(0)

        # Punctuation
        button_name = "."
        button = QtWidgets.QPushButton(button_name)
        button.setStyleSheet(self.DEFAULT_STYLESHEET)
        # adding button listener
        # button.clicked.connect(
        #     functools.partial(gui.keyboard.number_keyboard.NumberKeyboard.start_context,
        #                       keyboard_views))
        ret_context_switch_grid.addWidget(button, 0, 1, alignment=QtCore.Qt.AlignTop)
        self.character_buttons.append(button)

        # Numbers
        button_name = "0"
        button = QtWidgets.QPushButton(button_name)
        button.setStyleSheet(self.DEFAULT_STYLESHEET)
        # adding button listener
        button.clicked.connect(
            functools.partial(gui.keyboard.number_keyboard.NumberKeyboard.start_context,
                              keyboard_views))
        ret_context_switch_grid.addWidget(button, 0, 2, alignment=QtCore.Qt.AlignTop)
        self.character_buttons.append(button)

        # Emojis
        button_name = ":)"
        button = QtWidgets.QPushButton(button_name)
        button.setStyleSheet(self.DEFAULT_STYLESHEET)
        # adding button listener
        # button.clicked.connect(
        #     functools.partial(gui.keyboard.number_keyboard.NumberKeyboard.start_context,
        #                       keyboard_views))
        ret_context_switch_grid.addWidget(button, 0, 3, alignment=QtCore.Qt.AlignTop)
        self.character_buttons.append(button)

        # Enter
        button_name = u"\u21b5"

        button = QtWidgets.QPushButton(button_name)
        button.setStyleSheet(self.ENTER_STYLESHEET)
        # adding button listener
        button.clicked.connect(
            functools.partial(gui.keyboard.number_keyboard.NumberKeyboard.start_context,
                              keyboard_views))
        ret_context_switch_grid.addWidget(button, 0, 4, alignment=QtCore.Qt.AlignTop)
        self.character_buttons.append(button)

        # Backspace
        button_name = u"\u232b"

        button = QtWidgets.QPushButton(button_name)
        button.setStyleSheet(self.BKSP_STYLESHEET)
        # adding button listener
        button.clicked.connect(
            functools.partial(gui.keyboard.number_keyboard.NumberKeyboard.start_context,
                              keyboard_views))
        ret_context_switch_grid.addWidget(button, 0, 6, alignment=QtCore.Qt.AlignTop)
        self.character_buttons.append(button)

        return ret_context_switch_grid
