import functools
import math
import random
import string
import time

from PyQt5 import QtGui, QtWidgets, QtCore

import gui.keyboard.letter_keyboard
import gui.keyboard.number_keyboard
from nlp.complete import autocomplete


class Keyboards(QtWidgets.QWidget):

    def __init__(self, character_display_panel, interval):
        super().__init__()

        self.keyboard_views = QtWidgets.QStackedWidget()

        self.letter_keyboard = gui.keyboard.letter_keyboard.LetterKeyboard(self.keyboard_views,
                                                              character_display_panel,
                                                              interval)
        self.number_keyboard = gui.keyboard.number_keyboard.NumberKeyboard(self.keyboard_views,
                                                              character_display_panel,
                                                              interval)
        # self.number_keyboard = NumberKeyboard()

        self.keyboard_views.addWidget(self.letter_keyboard)
        self.keyboard_views.addWidget(self.number_keyboard)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.keyboard_views)
