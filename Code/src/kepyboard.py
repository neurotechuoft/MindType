import sys
from PyQt4 import QtGui


# function that returns print function to be used by on_click_listeners
def print_char(name):
    def print_char_function():
        # printing characters on same line
        print(name, end=""),
        sys.stdout.flush()

    return print_char_function  # (ButtonBlock --> extends QWidget)


class ButtonBlock(QtGui.QWidget):
    # constructor
    def __init__(self):
        super().__init__()

        buttons = []

        # creating a grid of buttons
        grid = QtGui.QGridLayout()
        for row in range(6):
            for col in range(6):
                button_name = chr(ord('a') + (row * 6) + col)
                button = QtGui.QPushButton(button_name)
                buttons.append(button)
                # adding buttons to grid and creating a listener (signals in python?)
                button.clicked.connect(print_char(button_name))
                grid.addWidget(button, row, col)
        # attaching grid to self
        self.setLayout(grid)

# Running gui
app = QtGui.QApplication(sys.argv)
buttonBlock = ButtonBlock()
buttonBlock.show()
sys.exit(app.exec_())
