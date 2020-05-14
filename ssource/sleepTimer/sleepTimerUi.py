# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class sleepTimerUi(QWidget):
    def __init__( self, x, y ):
        super( ).__init__( )
        self.setupUi( x, y )

    def setupUi(self, x, y):
        self.setObjectName("Form")
        self.resize(x, y)#212 145
        self.sleepTimeEdit = QtWidgets.QTimeEdit(self)
        self.sleepTimeEdit.setGeometry(QtCore.QRect(70, 10, 61, 21))
        self.sleepTimeEdit.setObjectName("sleepTimeEdit")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.label_2.setObjectName("label_2")
        self.wakeTimeEdit = QtWidgets.QTimeEdit(self)
        self.wakeTimeEdit.setGeometry(QtCore.QRect(70, 40, 61, 21))
        self.wakeTimeEdit.setObjectName("wakeTimeEdit")
        self.afterTimeEdit = QtWidgets.QLabel(self)
        self.afterTimeEdit.setGeometry(QtCore.QRect(10, 70, 81, 21))
        self.afterTimeEdit.setObjectName("afterTimeEdit")
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setGeometry(QtCore.QRect(90, 70, 41, 22))
        self.spinBox.setMaximum(59)
        self.spinBox.setObjectName("spinBox")
        self.applyButton = QtWidgets.QPushButton(self)
        self.applyButton.setGeometry(QtCore.QRect(140, 110, 61, 23))
        self.applyButton.setObjectName("applyButton")
        self.disableCheckBox1 = QtWidgets.QCheckBox(self)
        self.disableCheckBox1.setGeometry(QtCore.QRect(140, 10, 91, 21))
        self.disableCheckBox1.setObjectName("disableCheckBox1")
        self.disableCheckBox2 = QtWidgets.QCheckBox(self)
        self.disableCheckBox2.setGeometry(QtCore.QRect(140, 70, 91, 21))
        self.disableCheckBox2.setObjectName("disableCheckBox2")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.sleepTimeEdit.setDisplayFormat(_translate("Form", "hh:mm"))
        self.label.setText(_translate("Form", "Go to sleep:"))
        self.label_2.setText(_translate("Form", "Wake up:"))
        self.wakeTimeEdit.setDisplayFormat(_translate("Form", "hh:mm"))
        self.afterTimeEdit.setText(_translate("Form", "Sleep after:"))
        self.applyButton.setText(_translate("Form", "Apply"))
        self.disableCheckBox1.setText(_translate("Form", "Disable"))
        self.disableCheckBox2.setText(_translate("Form", "Disable"))
