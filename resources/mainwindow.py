import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog

import resources


class uiControlTest(QMainWindow):
    def __init__(self):
        super(uiControlTest, self).__init__()

        self.ui = uic.loadUi('main.ui')
        self.ui.show()

        self.ui.addButton.clicked.connect(lambda: self.awesomeButtonPressed())

    def awesomeButtonPressed(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter the desired name for your object:')

        if ok:
            x = resources.testWidget()
            list = self.ui.listView
            list.setModel()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = uiControlTest()
    sys.exit(app.exec_())
