# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TextFileWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class testWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self, parent=None)
        self.dynamic = QtWidgets.QWidget()
        self.setupUi()

    def setupUi(self):
        # Form.setObjectName("Form")
        # Form.resize(272, 80)
        self.dynamic.setGeometry(QtCore.QRect(0, 0, 271, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dynamic.sizePolicy().hasHeightForWidth())
        self.dynamic.setSizePolicy(sizePolicy)
        self.dynamic.setMaximumSize(QtCore.QSize(271, 80))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 112, 222))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 112, 222))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.dynamic.setPalette(palette)
        self.dynamic.setObjectName("dynamic")
        self.label = QtWidgets.QLabel(self.dynamic)
        self.label.setGeometry(QtCore.QRect(0, 0, 171, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.dynamic)
        self.lineEdit.setGeometry(QtCore.QRect(0, 20, 261, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(self.dynamic)
        self.checkBox.setGeometry(QtCore.QRect(200, 0, 64, 18))
        self.checkBox.setObjectName("checkBox")
        self.copyPath = QtWidgets.QPushButton(self.dynamic)
        self.copyPath.setGeometry(QtCore.QRect(0, 50, 75, 21))
        self.copyPath.setObjectName("copyPath")
        self.pushButton_8 = QtWidgets.QPushButton(self.dynamic)
        self.pushButton_8.setGeometry(QtCore.QRect(80, 50, 111, 21))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.dynamic)
        self.pushButton_9.setGeometry(QtCore.QRect(190, 50, 71, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(214, 214, 214))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(234, 234, 234))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.pushButton_9.setPalette(palette)
        self.pushButton_9.setObjectName("pushButton_9")
        self.line_6 = QtWidgets.QFrame(self.dynamic)
        self.line_6.setGeometry(QtCore.QRect(0, 70, 291, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")


        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Form", "Name"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Value"))
        self.checkBox.setText(_translate("Form", "Selected"))
        self.copyPath.setText(_translate("Form", "Copy Path"))
        self.pushButton_8.setText(_translate("Form", "Change Appearance"))
        self.pushButton_9.setText(_translate("Form", "PushButton"))
