import functools
import pyqtgraph as pg
import time
import timeit

from PyQt5 import QtGui, QtWidgets
from gui.keyboard.keyboards import Keyboards
from controller.MESSAGE import Message
from feature_flags.feature_flags import FeatureFlags
from openbci_board.board_setup import board_pause, board_start, safe_exit


class DevTools(QtWidgets.QDialog):
    def __init__(self, board, tagger_biosignal, main_controller, controllers, parent=None):
        super(DevTools, self).__init__(parent)

        self.start_time = timeit.default_timer()
        self.main_controller = main_controller
        self.controllers = [main_controller] + controllers

        self.board = board

        self.WINDOW_LEN = 3 * 256

        self.tagger_biosignal = tagger_biosignal

        self.pause_state = True

        # Creating main panel which contains everything
        self.main_panel = QtWidgets.QVBoxLayout()
        self.main_panel.setContentsMargins(0, 0, 0, 0)

        # creating header panel which has start, pause/resume and text display
        self.header_panel = QtWidgets.QHBoxLayout()
        self.main_panel.addLayout(self.header_panel)

        # creating header panel buttons
        self.play_pause_button = QtWidgets.QPushButton("Play/Pause")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.load_button = QtWidgets.QPushButton("Load")
        self.save_button = QtWidgets.QPushButton("Save")

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
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(0)

        # attaching grid to main panel
        self.main_panel.addLayout(self.grid)

        self.tag_buttons = []

        self.curr_tag = 0

        # adding tag buttons to the grid)
        for row in range(2):
            for col in range(5):
                character_number = (row * 6) + col
                button = QtWidgets.QPushButton(str(character_number))
                # button.setStyleSheet("QPushButton {background-color: black; color: white; font-size: 65px;}")

                # adding button listener
                button.clicked.connect(functools.partial(self.tag, character_number))
                self.grid.addWidget(button, row, col)
                self.tag_buttons.append(button)

        # # PyQtGraph
        # self.pw = pg.PlotWidget(self)
        # self.pw.showGrid(x=True, y=True)
        # self.pw.setDownsampling(mode='peak')
        # self.pw.setClipToView(True)
        # self.pw.setXRange(0, 3.0)
        # self.pw.setYRange(-1.0, 1.0)
        # # Plot details
        # self.colours = [QtGui.QColor(226, 0, 26),  # red
        #                 QtGui.QColor(255, 106, 0),  # orange
        #                 QtGui.QColor(255, 176, 0),  # yellow
        #                 QtGui.QColor(123, 204, 0),  # green
        #                 QtGui.QColor(11, 191, 217),  # torquoise
        #                 QtGui.QColor(11, 98, 217),  # blue
        #                 QtGui.QColor(0, 74, 173),  # navy
        #                 QtGui.QColor(106, 11, 228),  # purple
        #                 QtGui.QColor(20, 20, 20),  # black
        #                 ]
        # self.graphs = []
        # for colour in self.colours:
        #     self.graphs.append(self.pw.plot(pen=pg.mkPen(colour)))
        #
        # # Timer for updating Graph
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.graph_update)
        #
        # # creating a graph grid
        # self.graph_layout = QtWidgets.QHBoxLayout()
        #
        # self.graph_layout.addWidget(self.pw)
        # self.main_panel.addLayout(self.graph_layout)

        # setting layout to main_panel
        self.setLayout(self.main_panel)

    def play_pause(self):
        print("play-pause")
        if self.pause_state:
            self.send_msg_to_controllers(Message.START)
            board_start(self.board, self.start_time, self.tagger_biosignal)
        else:
            self.send_msg_to_controllers(Message.PAUSE)
            board_pause(self.board)

        self.pause_state = not self.pause_state
        # if self.controller.peek() is Message.PAUSE:
        #     self.controller.send(Message.START)
        # else: self.controller.pause()


    def stop(self):
        print("stop")
        # self.controller.quit()
        self.send_msg_to_controllers(Message.EXIT)

    def load(self):
        print("load")

    def save(self):
        print("save")

    def tag(self, tag_number):
        self.curr_tag = tag_number
        self.send_msg_to_controllers(tag_number)

    def get_current_tag(self):
        return self.curr_tag

    def send_msg_to_controllers(self, message):
        for controller in self.controllers:
            controller.send(message)

    # def graph_update(self):
    #     self.tagger_biosignal.process_graph(256.0)
    #     for i in range(0, len(self.graphs) - 1):
    #         self.graphs[i].setData(self.tagger_biosignal.graph_samples[i])
    #
    #     self.graphs[len(self.graphs) - 1].setData(self.tagger_biosignal.graph_tag)
    #
    #     time.sleep(1.0 / 20.0)

    def closeEvent(self, event):
        # safe_exit_confirmed = False

        # self.send_msg_to_controllers(Message.EXIT)

        # while not safe_exit_confirmed:
        #     if self.main_controller.search(Message.SAFE_TO_EXIT):
        #         safe_exit_confirmed = True

        # self.main_controller.send(Message.GUI_EXIT)
        if FeatureFlags.BOARD:
            self.send_msg_to_controllers(Message.EXIT)

            safe_exit(self.board, self.main_controller, [self.tagger_biosignal,])

            self.main_controller.send(Message.GUI_EXIT)

        pg.exit()
        event.accept()
