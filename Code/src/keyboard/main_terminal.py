# main method
# -----------
import sys

from PyQt4 import QtGui

from MindType import MindType

if __name__ == '__main__':
    # Running gui
    app = QtGui.QApplication(sys.argv)
    mindType = MindType()
    mindType.resize(550, 550)
    mindType.show()
    sys.exit(app.exec_())
