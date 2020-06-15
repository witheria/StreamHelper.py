from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout,
                             QPushButton)

# Initialize application
from resources.windows.test import Fenster

app = QApplication([])

# Create label
label = QLabel('Zzzzz')


def say_hello(event):
    label.setText('Hello, world!')


# Create button
button = QPushButton('Press me!')
button.clicked.connect(say_hello)

# Create layout and add widgets
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)
layout.addWidget(Fenster)

# Apply layout to widget
widget = QWidget()
widget.setLayout(layout)

widget.show()

app.exec_()
