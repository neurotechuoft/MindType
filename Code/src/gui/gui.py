import gui.keyboard.letter_keyboard
import json

from PyQt5 import QtGui, QtCore, QtWidgets

# Sayan sucks; don't complain - yours truly Abdel and Scholar
# ^ Sayan is
from gui.keyboard.keyboards import Keyboards
from controller.MESSAGE import Message
from feature_flags.feature_flags import FeatureFlags


class GUI(QtWidgets.QWidget):
    def __init__(self, main_controller, controllers, parent=None):
        super(GUI, self).__init__(parent)

        self.views = QtWidgets.QStackedWidget()

        self.keyboard_gui = gui.keyboard.keyboard_gui.KeyboardGUI(main_controller, controllers)

        self.setup_gui = gui.setup_gui.SetupGUI()

        self.views.addWidget(self.setup_gui)
        self.views.addWidget(self.keyboard_gui)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.views)

    def confirm_initial_setup_finished(self):
        setup = {}
        
        with open("./../config.json") as setup_file:
            setup = json.loads(setup_file)
            setup["initial_setup"] = True
        
        with open("./../config.json", "w") as setup_file:
            json.dumps(setup, setup_file)