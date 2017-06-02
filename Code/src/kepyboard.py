import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)
widget = QtGui.QWidget()
layout = QtGui.QGridLayout()

buttons = {}

for i in range(6):
    for j in range(6):
        # keep a reference to the buttons
        buttons[i, j] = QtGui.QPushButton(chr(ord('a') + (i*6) + j))
        # add to the layout
        layout.addWidget(buttons[i, j], i, j)

widget.setLayout(layout)
widget.show()
sys.exit(app.exec_())
