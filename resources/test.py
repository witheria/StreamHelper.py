from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys

from qtpy import uic

from resources.runtime import savestate


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('uis' + savestate.symbol + 'settings.ui')
        self.ui.setWindowTitle("Spoon")


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        if self.w is None:
            self.w = AnotherWindow()
            self.w.ui.show()

        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()