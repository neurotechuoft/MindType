import functools

from PyQt4 import QtGui


class DevTools(QtGui.QDialog):
    def __init__(self, controller, parent=None):
        super(DevTools, self).__init__(parent)

        self.controller = controller

        # Creating main panel which contains everything
        self.main_panel = QtGui.QVBoxLayout()
        self.main_panel.setContentsMargins(0, 0, 0, 0)

        # creating header panel which has start, pause/resume and text display
        self.header_panel = QtGui.QHBoxLayout()
        self.main_panel.addLayout(self.header_panel)

        # creating header panel buttons
        self.play_pause_button = QtGui.QPushButton("Play/Pause")
        self.stop_button = QtGui.QPushButton("Stop")
        self.load_button = QtGui.QPushButton("Load")
        self.save_button = QtGui.QPushButton("Save")

        # setting button click listeners
        self.play_pause_button.clicked.connect(functools.partial(self.play_pause))
        self.stop_button.clicked.connect(functools.partial(self.stop))
        self.load_button.clicked.connect(functools.partial(self.load))
        self.save_button.clicked.connect(functools.partial(self.save))

        # adding buttons to header panel
        self.header_panel.addWidget(self.play_pause_button)
        self.header_panel.addWidget(self.stop_button)
        self.header_panel.addWidget(self.load_button)
        self.header_panel.addWidget(self.save_button)

        # creating a button grid
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)

        # attaching grid to main panel
        self.main_panel.addLayout(self.grid)

        self.tag_buttons = []

        self.curr_tag = 0

        # adding keyboard buttons to the grid)
        for row in range(2):
            for col in range(5):
                character_number = (row * 6) + col
                button = QtGui.QPushButton(str(character_number))
                # button.setStyleSheet("QPushButton {background-color: black; color: white; font-size: 65px;}")

                # adding button listener
                button.clicked.connect(functools.partial(self.tag, character_number))
                self.grid.addWidget(button, row, col)
                self.tag_buttons.append(button)

        # setting layout to main_panel
        self.setLayout(self.main_panel)

    def play_pause(self):
        print("play-pause")
        if self.controller.paused:
            self.controller.resume()
        else: self.controller.pause()


    def stop(self):
        print("stop")
        self.controller.quit()


    def load(self):
        print("load")

    def save(self):
        print("save")

    def tag(self, tag_number):
        self.curr_tag = tag_number
        self.controller.set_tag(tag_number)

    def get_current_tag(self):
        return self.curr_tag
