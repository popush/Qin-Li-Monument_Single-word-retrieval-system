# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'review.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import cv2 as cv
import sys


class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)
        # print("x0:%d\tx1%d"%(self.x0,self.x1))
        # print("y0:%d\ty1%d" % (self.y0, self.y1))

    def get_rec(self):
        return self.x0, self.x1, self.y0, self.y1


class point_Label(QLabel):
    x = 0
    y = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x = event.x()
        self.y = event.y()
        self.update()

    def get_point(self):
        return self.x,self.y

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 10, Qt.SolidLine))
        painter.drawPoint(self.x,self.y)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(539, 641)
        self.label_print = QtWidgets.QLabel(Form)
        self.label_print.setGeometry(QRect(10, 10, 381, 621))
        self.label_print.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.label_print.setText("")
        self.label_print.setAlignment(QtCore.Qt.AlignCenter)
        self.label_print.setObjectName("label")

        self.label_auto = QtWidgets.QLabel(Form)
        self.label_auto = point_Label(self)
        self.label_auto.setGeometry(QRect(10, 10, 381, 621))
        self.label_auto.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.label_auto.setText("")
        self.label_auto.setAlignment(QtCore.Qt.AlignCenter)
        self.label_auto.setObjectName("label")


        self.label = QtWidgets.QLabel(Form)
        self.label = MyLabel(self)  # 重定义的label
        self.label.setGeometry(QRect(10, 10, 381, 621))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(400, 340, 131, 51))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 410, 131, 51))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(400, 480, 131, 51))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(400, 20, 131, 301))
        font = QtGui.QFont()
        font.setFamily("書體坊顏體㊣")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "裁切纠错"))
        self.pushButton.setText(_translate("Form", "手动裁切"))
        self.pushButton_2.setText(_translate("Form", "自动裁切"))
        self.pushButton_3.setText(_translate("Form", "确 定"))
        self.label_2.setText(_translate("Form", "提示：\n"
                                                "手动裁切：\n"
                                                "\n"
                                                "将使用您手动\n"
                                                "切割的范围\n"
                                                "作为保存图片\n"
                                                "的依据。\n"
                                                "自动裁切：\n"
                                                "\n"
                                                "使用区域扩张法\n"
                                                "进行单字切割\n"
                                                "请尽量\n"
                                                "点击单字中心！"))
