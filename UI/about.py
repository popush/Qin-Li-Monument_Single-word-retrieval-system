# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 240)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 301, 51))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 301, 111))
        font = QtGui.QFont()
        font.setFamily("方正字迹-管峻楷书繁体")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(214, 202, 101, 31))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "关于本程序"))
        self.label.setText(_translate("Form", "《勤礼碑》单字检索系统"))
        self.label_2.setText(_translate("Form", "作者：王会元\n"
                                                "导师：张九龙\n"
                                                "院系：西安理工大学计算机学院\n"
                                                "时间： 2019.\n"
                                                "类型：毕业设计"))
        self.pushButton.setText(_translate("Form", "确 定"))
