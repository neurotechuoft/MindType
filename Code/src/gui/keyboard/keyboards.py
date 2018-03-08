import functools
import math
import random
import string
import time

from PyQt5 import QtGui, QtWidgets, QtCore

from gui.keyboard.letter_keyboard import LetterKeyboard
from nlp.complete import autocomplete


class Keyboards(QtWidgets.QWidget):

    def __init__(self, character_display_panel, interval):
        super()

        self.keyboard_views = QtWidgets.QStackedWidget()

        self.letter_keyboard = LetterKeyboard(self.keyboard_views,
                                              character_display_panel,
                                              interval)
        # self.number_keyboard = NumberKeyboard()

        self.keyboard_views.addWidget(self.letter_keyboard)
        self.keyboard_views.addWidget(self.number_keyboard)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.keyboard_views)

