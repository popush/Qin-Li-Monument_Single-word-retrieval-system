# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'single_scan.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(460, 344)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 30, 221, 221))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(270, 200, 171, 51))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 282, 81, 31))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(170, 282, 81, 31))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(280, 50, 121, 71))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(280, 30, 151, 21))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(270, 260, 171, 51))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(14)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "单字浏览"))
        self.label.setText(_translate("Form", ""))
        self.pushButton.setText(_translate("Form", "进入原图"))
        self.pushButton_2.setText(_translate("Form", "上一张"))
        self.pushButton_3.setText(_translate("Form", "下一张"))
        self.label_2.setText(_translate("Form", "TextLabel"))
        self.label_3.setText(_translate("Form", "这个字是："))
        self.pushButton_4.setText(_translate("Form", "单字检索"))


