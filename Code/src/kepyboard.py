import functools
import sys

from random import randint
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer

def print_char(name):
    def print_char_function():
        # printing characters on same line
        print(name)
        sys.stdout.flush()

    return print_char_function  # (ButtonBlock --> extends QWidget)

# grid of labels object
class ButtonBlock(QtGui.QWidget):
    grid = QtGui.QGridLayout()
    vbox = QtGui.QVBoxLayout()

    # constructor
    def __init__(self):
        super(ButtonBlock, self).__init__()
        # creating a grid of buttons, setting margins and spacing
        ButtonBlock.grid.setSpacing(0)
        ButtonBlock.vbox.setContentsMargins(0, 0, 0, 0)
        label2 = QtGui.QLabel("aylmao")
        ButtonBlock.vbox.addWidget(label2)
        # loops through and adds labels with appropriate characters
        for i in range(6):
            for j in range(6):
                button_name = chr(ord('a') + (i * 6) + j)
                label = QtGui.QLabel(button_name)
                label.setStyleSheet(
                    "QLabel {background-color: black; color: white;qproperty-alignment: AlignCenter; font-size: 35px;}")
                # adding buttons to grid and creating a listener (signals in python?)
                ButtonBlock.grid.addWidget(label, i, j)
        # attaching grid to self
        ButtonBlock.vbox.addLayout(ButtonBlock.grid)
        self.setLayout(ButtonBlock.vbox)

# function that lightens a row of widgets
def lighten(block, index):
    for x in range(6):
        letter = chr(ord('a') + (index * 6) + x)
        label = QtGui.QLabel(letter)
        label.setStyleSheet(
            "QLabel {background-color: black; color: white; qproperty-alignment: AlignCenter; font-size: 35px;}")
        block.grid.addWidget(label, index, x)

# function that darkens a row of widgets
def darken(block, index):
    for x in range(6):
        letter = chr(ord('a') + (index * 6) + x)
        label = QtGui.QLabel(letter)
        label.setStyleSheet(
            "QLabel {background-color: black; color: blue; qproperty-alignment: AlignCenter; font-size: 35px;}")
        block.grid.addWidget(label, index, x)

# function that darkens a column of widgets
def vertdark(block,index):
    for x in range(6):
        letter = chr(ord('a') + index + (x * 6))
        label = QtGui.QLabel(letter)
        label.setStyleSheet(
            "QLabel {background-color: black; color: blue; qproperty-alignment: AlignCenter; font-size: 35px;}")
        block.grid.addWidget(label, x, index)

# function that lightens a column of widgets
def vertlight(block,index):
    for x in range(6):
        letter = chr(ord('a') + index + (x * 6))
        label = QtGui.QLabel(letter)
        label.setStyleSheet(
            "QLabel {background-color: black; color: white; qproperty-alignment: AlignCenter; font-size: 35px;}")
        block.grid.addWidget(label, x, index)

# calls the flashes in sequence
def flash(block, index, isrow):
    if isrow:
        darkobj = functools.partial(darken,block,index)
        lightobj = functools.partial(lighten,block,index)
        QTimer.singleShot(0, darkobj)
        QTimer.singleShot(200,lightobj)
    else:
        darkobj = functools.partial(vertdark, block, index)
        lightobj = functools.partial(vertlight, block, index)
        QTimer.singleShot(0, darkobj)
        QTimer.singleShot(200, lightobj)

# driver method for flash function
# checks that all rows and columns has been flashed at least once
def runFlash(block):
    complete = False
    beenflashed = [False] * 12
    counter = 300
    while complete == False:
        isrow = False
        index = randint(0,11)
        beenflashed[index] = True
        if(index>5):
            index=index-6
            isrow = True
        timercallback = functools.partial(flash, block, index, isrow)
        QTimer.singleShot(counter, timercallback)
        counter += 300
        complete = all(beenflashed)

# Running gui
app = QtGui.QApplication(sys.argv)
buttonBlock = ButtonBlock()
runFlash(buttonBlock)
buttonBlock.show()
buttonBlock.resize(400, 400)
sys.exit(app.exec_())
