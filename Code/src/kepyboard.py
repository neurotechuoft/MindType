import functools
import sys

from random import randint
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer

# grid of labels object
class ButtonBlock(QtGui.QWidget):
    grid = QtGui.QGridLayout()
    vbox = QtGui.QVBoxLayout()
    hbox = QtGui.QHBoxLayout()
    display = ""

    # constructor
    def __init__(self):
        super(ButtonBlock, self).__init__()
        # creating a grid of buttons, setting margins and spacing
        ButtonBlock.grid.setSpacing(0)
        ButtonBlock.vbox.setContentsMargins(0, 0, 0, 0)

        typed = QtGui.QLabel("")
        startbut = QtGui.QPushButton("Start/next letter")
        endbut = QtGui.QPushButton("Finished")

        send = functools.partial(runFlash, self)

        startbut.clicked.connect(send)
        endbut.clicked.connect(print_char('+',self))

        ButtonBlock.hbox.addWidget(typed)
        ButtonBlock.hbox.addWidget(startbut)
        ButtonBlock.hbox.addWidget(endbut)

        # loops through and adds labels with appropriate characters
        for i in range(6):
            for j in range(6):
                character_number = (i * 6) + j

                if character_number < 26:
                    button_name = chr(ord('a') + character_number)

                else:
                    button_name = str(character_number - 26)
                #button_name = chr(ord('a') + (i * 6) + j)
                label = QtGui.QPushButton(button_name)
                label.setStyleSheet(
                    "QLabel {background-color: black; color: white; font-size: 65px;}")
                # adding buttons to grid and creating a listener (signals in python?)
                label.clicked.connect(print_char(button_name,self))
                ButtonBlock.grid.addWidget(label, i, j)

        # attaching grid to self
        ButtonBlock.vbox.addLayout(ButtonBlock.hbox)
        ButtonBlock.vbox.addLayout(ButtonBlock.grid)
        self.setLayout(ButtonBlock.vbox)

def deleteWidget(block, index):
    item = block.hbox.itemAt(index)
    if item is not None:
        widget = item.widget()
        if widget is not None:
            block.hbox.removeWidget(widget)
            widget.deleteLater()
# function that lightens a row of widgets

def lighten(block, index):
    for x in range(6):
        letter = chr(ord('a') + (index * 6) + x)
        label = QtGui.QPushButton(letter)
        label.setStyleSheet(
            "QPushButton {background-color: black; color: white; font-size: 65px;}")
        label.clicked.connect(print_char(letter, block))
        block.grid.addWidget(label, index, x)

# function that darkens a row of widgets
def darken(block, index):
    for x in range(6):
        letter = chr(ord('a') + (index * 6) + x)
        label = QtGui.QPushButton(letter)
        label.setStyleSheet(
            "QPushButton {background-color: black; color: blue; font-size: 65px;}")
        label.clicked.connect(print_char(letter, block))
        block.grid.addWidget(label, index, x)

# function that darkens a column of widgets
def vertdark(block,index):
    for x in range(6):
        letter = chr(ord('a') + index + (x * 6))
        label = QtGui.QPushButton(letter)
        label.setStyleSheet(
            "QPushButton {background-color: black; color: blue; font-size: 65px;}")
        label.clicked.connect(print_char(letter,block))
        block.grid.addWidget(label, x, index)

# function that lightens a column of widgets
def vertlight(block,index):
    for x in range(6):
        letter = chr(ord('a') + index + (x * 6))
        label = QtGui.QPushButton(letter)
        label.setStyleSheet(
            "QPushButton {background-color: black; color: white; font-size: 65px;}")
        label.clicked.connect(print_char(letter, block))
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

def print_char(name, block):
    def print_char_function():
        # printing characters on same line
        print(name)
        if name != '+':
            block.display = block.display + name
            type = QtGui.QLabel(block.display)
            block.hbox.insertWidget(0,type)
            deleteWidget(block,1)
        else:
            type = QtGui.QLabel("")
            block.display = ""
            block.hbox.insertWidget(0, type)
            deleteWidget(block, 1)
            print("done")
    return print_char_function  # (ButtonBlock --> extends QWidget)

def initflash(block):
    for x in range(6):
        flash(block, x, True)
    for x in range(6):
        flash(block, x, False)

# Running gui
app = QtGui.QApplication(sys.argv)
buttonBlock = ButtonBlock()
initflash(buttonBlock)
buttonBlock.show()
buttonBlock.resize(550, 500)
sys.exit(app.exec_())
