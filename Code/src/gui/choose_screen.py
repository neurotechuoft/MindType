import functools
import sys

from PyQt4 import QtGui, QtCore

from controller import Controller
from gui.dev_tools import DevTools
from gui.keyboard.gui import GUI


class ChooseScreen(QtGui.QWidget):
    def __init__(self, controller, parent=None):
        super(ChooseScreen, self).__init__(parent)

        # Creating main panel which contains everything
        self.main_panel = QtGui.QVBoxLayout()
        self.main_panel.setContentsMargins(0, 0, 0, 0)

        # creating header panel which has start, pause/resume and text display
        self.header_panel = QtGui.QHBoxLayout()
        self.main_panel.addLayout(self.header_panel)

        # creating header panel buttons
        # self.character_display_panel = QtGui.QLabel("Enter Text!")
        self.dev_tools_button = QtGui.QPushButton("Dev Tools")
        self.keyboard_button = QtGui.QPushButton("Keyboard")

        # setting button click listeners
        self.dev_tools_button.clicked.connect(functools.partial(self.start_dev_tools))
        self.keyboard_button.clicked.connect(functools.partial(self.start_keyboard))

        # adding buttons to header panel
        # self.header_panel.addWidget(self.character_display_panel)
        self.header_panel.addWidget(self.dev_tools_button)
        self.header_panel.addWidget(self.keyboard_button)

        # adding keyboard gui to main panel
        # creating a button grid
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)

        self.main_panel.addLayout(self.grid)

        # setting layout to main_panel
        self.setLayout(self.main_panel)

        self.keyboard_screen_gui = GUI(controller)
        self.dev_tools_gui = DevTools(controller)

    @QtCore.pyqtSlot()
    def start_dev_tools(self):
        self.dev_tools_gui.exec_()

    @QtCore.pyqtSlot()
    def start_keyboard(self):
        self.keyboard_screen_gui.exec_()


if __name__ == '__main__':
    # Running gui
    app = QtGui.QApplication(sys.argv)
    main_scr = ChooseScreen(Controller())
    main_scr.resize(500, 100)
    main_scr.show()
    sys.exit(app.exec_())
