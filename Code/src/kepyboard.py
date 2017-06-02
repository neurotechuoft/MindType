import sys
from PyQt4 import QtGui


class ButtonBlock(QtGui.QWidget):
    def __init__(self, *args):
        super(QtGui.QWidget, self).__init__()
        grid = QtGui.QGridLayout()

        for i in range(6):
            for j in range(6):
                buttonName = chr(ord('a') + (i * 6) + j)
                button = QtGui.QPushButton(buttonName, self)
                # add to the layout
                button.clicked.connect(self.make_calluser(buttonName))
                grid.addWidget(button, i, j)
        self.setLayout(grid)

    def make_calluser(self, name):
        def calluser():
            print (name, end=""),
            sys.stdout.flush()

        return calluser


app = QtGui.QApplication(sys.argv)
buttonBlock = ButtonBlock()
buttonBlock.show()
sys.exit(app.exec_())
