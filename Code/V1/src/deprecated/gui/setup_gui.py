import functools
import math
import random
import string
import time

from PyQt5 import QtGui, QtWidgets, QtCore

import gui.keyboard.letter_keyboard
import gui.keyboard.number_keyboard
from nlp.complete import autocomplete


class SetupGUI(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.interval = 100

        self.layout = QtWidgets.QVBoxLayout()