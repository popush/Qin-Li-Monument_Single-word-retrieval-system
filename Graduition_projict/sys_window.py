from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2 as cv
import os
import sys
from Graduition_projict import thread1 as th
from Graduition_projict import box
from Graduition_projict import golbal as gv
from Alex_Net import sus_one_pic as forecast
from Alex_Net import  suspict
import time
import threading
import inspect
import ctypes

"""----------------------------------------------------------------------------"""
from UI.Main_window import Ui_MainWindow
from UI.about import Ui_Form as about_dialog
from UI.scan_rubbing import Ui_Form as scan_rubbing
from UI.cut import Ui_Form as cut_dialog
from UI.result import Ui_Form as result_dialog
from UI.review import Ui_Form as review_dialog
from UI.single_scan import Ui_Form as single_dialog
from UI.search import Ui_Form as search_dialog
from UI.same_scan import Ui_Form as same_scan
from UI.setting import Ui_Form as setting_dialog
from UI.help import Ui_Form as help_dialog
"""----------------------------------------------------------------------------"""
img_list = []       #导入的图像列表
scan_index = 0

res_list = []       #经过预测后的图像列表
res_index = 0

final_list = []     #校准后的最终图像
final_index = 0

t_list = []         #单字查询结果用
t_index = 0
"""主窗口==========导入窗口"""
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setFixedSize(710, 517)
        self.img_list = []  # 处理的图片列表
        self.setupUi(self)
        gv.laber_help()
        gv.init_forecast_label()
        gv.init_final_label()


    def input_img(self):
        filepath = QFileDialog.getExistingDirectory(self,
                                                    "选取碑帖文件所在文件夹",
                                                    "C:/")
        if len(filepath) != 0:
            gv.rootdir = filepath
            dir_list = os.listdir(filepath)
            i = 0
            length = len(dir_list)
            while i < length:  # 将路径写入全局变量list中
                path = os.path.join(filepath, dir_list[i])
                if os.path.isfile(path):
                    if (th.is_img(path)):
                        img_list.append(path)
                i += 1

    def set_output(self):
        filepath = QFileDialog.getExistingDirectory(self,
                                                    "选取输出文件夹",
                                                    gv.rootdir)
        if len(filepath) != 0:
            gv.output_dir = filepath
        print('已设置输出路径为：\n' + filepath)

    def closeEvent(self, *args, **kwargs):
        sys.exit(app.exec_())
"""-----------------------------------------------------------------------------------------------"""
"""’关于‘窗口========"""
class AboutWindow(QWidget, about_dialog):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__()
        self.setupUi(self)

    def open(self):
        self.show()
"""-----------------------------------------------------------------------------------------------"""
"""’浏览碑帖‘窗口========"""
class Scan_rubbing(QWidget, scan_rubbing):
    def __init__(self, parent=None):
        super(Scan_rubbing, self).__init__()
        self.setupUi(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.pushButton.clicked.connect(self.left)
        self.pushButton_2.clicked.connect(self.right)

    def open(self):
        if len(img_list) == 0 or img_list == None:
            self.show_message()
        else:
            self.display(img_list[scan_index])
            self.show()

    def show_message(self):
        QMessageBox.information(self, "提示", "\n尚未导入图像\t\n", QMessageBox.Ok)

    def display(self, path):
        # cv.imread(path)
        self.label.setPixmap(QPixmap(""))
        img = QtGui.QPixmap(path).scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(img)

    def left(self):
        global scan_index
        if scan_index == 0:
            scan_index = len(img_list) - 1
            self.display(img_list[scan_index])
        else:
            scan_index -= 1
            self.display(img_list[scan_index])

    def right(self):
        global scan_index
        if scan_index == len(img_list) - 1:
            scan_index = 0
            self.display(img_list[scan_index])
        else:
            scan_index += 1
            self.display(img_list[scan_index])
"""-----------------------------------------------------------------------------------------------"""
"""’切割碑帖‘窗口========"""
class CutWindow(QWidget, cut_dialog):
    def __init__(self, parent=None):
        super(CutWindow, self).__init__()
        self.setupUi(self)
        self.res = res_Window()
        self.pushButton.clicked.connect(self.cut)
        self.pushButton_2.clicked.connect(self.sus)
        self.pushButton_3.clicked.connect(self.res.open)
        self.c = threading.Thread(target=th.cut_begin)
        self.c.setDaemon(True)
        self.begin_flag = False
        self.printed = False

    def show_message(self, title, text):
        QMessageBox.information(self, title, text, QMessageBox.Ok)

    def open(self):
        if self.printed == False:
            self.textEdit.setText("进行处理前，请先设置处理文件目录（以及输出目录）\n当前处理文件目录：\n" + gv.rootdir + '\n')

        self.show()

    def cut(self):
        if self.begin_flag == False:
            if gv.rootdir == "":
                self.show_message("提示", "请设置图片所在目录")
            else:
                self.show_message("提示", "已经开始处理，请耐心等待")
                self.textEdit.setText("载入文件目录：\n" + gv.rootdir + "\n输出目录：\n" + gv.output_dir + '\n')
                self.begin_flag = True
                self.printed = True
                self.c.start()
            # self.begin_flag = False
        else:
            self.show_message("提示", "正在处理中请稍后\n或已处理完成")

    def closeEvent(self, QCloseEvent):
        # if self.begin_flag == True:
        #     self.show_message("提示", "程序将继续进行，但请勿退出主程序")
        # else:
        QCloseEvent.accept()
    def sus(self):
        # suspict.forecast()
        p = threading.Thread(target=suspict.forecast)
        p.setDaemon(True)
        p.start()
"""-----------------------------------------------------------------------------------------------"""
"""’查看切割结果‘窗口========"""
class res_Window(QWidget, result_dialog):
    def __init__(self, parent=None):
        super(res_Window, self).__init__()
        self.setupUi(self)
        self.review = rvw_Window()
        self.pushButton_2.clicked.connect(self.left)
        self.pushButton_3.clicked.connect(self.right)
        self.pushButton.clicked.connect(self.review.open)
        self.pushButton_4.clicked.connect(self.set_final_result)
        self.pushButton_5.clicked.connect(self.delate)

    def show_message(self, title, text):
        QMessageBox.information(self, title, text, QMessageBox.Ok)

    def open(self):
        path = os.path.join(gv.output_dir, 'single')
        gv.init_forecast_label()
        if len(gv.forecast_label) == 0:
            self.show_message("提示","请先对字符进行分类")
        else:
            if os.path.exists(path):
                dir_list = os.listdir(path)
                i = 0
                length = len(dir_list)
                while i < length:
                    res_path = os.path.join(path, dir_list[i])
                    if os.path.isfile(res_path):
                        if (th.is_img(res_path)):
                            res_list.append(res_path)
                    i += 1
                # print(res_list)
                self.display(res_list[res_index])
                # self.label_3.setText(gv.forecast_label[res_list[res_index]])
                self.show()


            else:
                self.show_message("提示", "文件尚未开始处理\n请点击开始按钮处理程序！")

    def display(self, path):
        # cv.imread(path)
        self.label_3.setText("")
        self.label.setPixmap(QPixmap(""))
        img = QtGui.QPixmap(path).scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(img)
        sub = path.split("\\")
        # print(sub[len(sub) - 1])
        name = sub[len(sub) - 1]
        self.label_2.setText("文件名：\n" + name)
        # self.label_3.setText(gv.forecast_label[res_list[res_index]])
        if gv.forecast_label:
            if res_list[res_index] in gv.forecast_label:
                # print(gv.forecast_label)
                fore = gv.forecast_label[res_list[res_index]]
                if len(fore) == 1:
                    self.label_3.setText("预测为：\n"+gv.ch[str(fore[0])])
                if len(fore) == 2:
                    self.label_3.setText("预测为：\n" + gv.ch[str(fore[0])]+"或者:\n"+gv.ch[str(fore[1])])

            else:
                # print(res_list[res_index])
                print('')

    def left(self):
        global res_index
        if res_list[res_index] in gv.forecast_label.keys():
            gv.final_append(res_list[res_index], gv.forecast_label[res_list[res_index]])
        if res_index == 0:
            res_index = len(res_list) - 1
            self.display(res_list[res_index])
        else:
            res_index -= 1
            self.display(res_list[res_index])


    def right(self):
        global res_index
        if res_list[res_index] in gv.forecast_label.keys():
            gv.final_append(res_list[res_index], gv.forecast_label[res_list[res_index]])
        if res_index == len(res_list) - 1:
            res_index = 0
            self.display(res_list[res_index])
        else:
            res_index += 1
            self.display(res_list[res_index])


    def delate(self):
        os.remove(res_list[res_index])
        del res_list[res_index]

    def set_final_result(self):
        str = self.textEdit.toPlainText()
        self.textEdit.setText('')
        if len(str) == 0 or str =='':
            gv.final_append(res_list[res_index],gv.forecast_label[res_list[res_index]])
            self.show_message("提示","未输入字符，若识别正确，\n直接点击下一张或上一张即可！")
        else:
            # temp_result = []
            temp_result = gv.get_laber_key(gv.ch,str)
            if temp_result[0]!= 'false':
                gv.forecast_append(res_list[res_index],temp_result)
                gv.final_append(res_list[res_index],temp_result)
                print(temp_result[0])
                # print(temp_result[0])
                # print(gv.final_label)
            # print(gv.final_label)
            else:
                self.show_message('提示','输入字符不在《勤礼碑》中！')
            # print(temp_result)
            # print(str)
            # self.show_message("2", str)
"""-----------------------------------------------------------------------------------------------"""
"""’结果修改‘窗口========"""
class rvw_Window(QWidget, review_dialog):
    def __init__(self, parent=CutWindow):
        super(rvw_Window, self).__init__()
        self.auto = False
        self.hand = False
        self.setupUi(self)
        self.label.hide()
        self.label_auto.hide()
        self.pushButton.clicked.connect(self.cut_by_hand)
        self.pushButton_3.clicked.connect(self.select)
        self.pushButton_2.clicked.connect(self.cut_auto)

    def open(self):
        self.path()
        self.display(self.org_path)
        self.show()

    def path(self):
        global res_index
        full_name = res_list[res_index]
        # print(full_name)
        sub = full_name.split("\\")
        sub_last = sub[len(sub) - 1]
        # print(sub_last)
        ext = sub_last.split('.')
        name = sub_last.split('(')
        final_name = name[0] + '.' + ext[len(ext) - 1]
        # print(final_name)
        self.org_path = os.path.join(gv.rootdir, final_name)

    def display(self, path):
        self.path()
        self.label.hide()
        self.label_auto.hide()
        self.label_print.setPixmap(QPixmap(""))
        img = QtGui.QPixmap(path).scaled(self.label_print.width(), self.label_print.height(), Qt.KeepAspectRatio)
        self.label_print.setPixmap(img)
        # print('ok')

    def cut_by_hand(self):
        self.path()
        self.hand = True
        # self.label_print.show()
        self.label_print.hide()
        self.label_auto.hide()
        self.label.setPixmap(QPixmap(""))
        img = QtGui.QPixmap(self.org_path).scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(img)
        self.label.show()

    def cut_auto(self):
        self.auto = True
        self.label.hide()
        self.label_print.hide()
        self.label_auto.setPixmap(QPixmap(""))
        img = QtGui.QPixmap(self.org_path).scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label_auto.setPixmap(img)
        self.label_auto.show()



    def show_message(self, title, text):
        QMessageBox.information(self, title, text, QMessageBox.Ok)

    def select(self):
        self.path()
        if self.hand == False and self.auto == False:
            self.show_message("提示","请选择切割方式！")
        if self.hand == True:
            x0, x1, y0, y1 = self.label.get_rec()
            img = cv.imread(self.org_path)
            h, w, c = img.shape
            if h / w > 621 / 381:
                rate = h / 621.0
                # print(rate)
                side = (381 - (w / rate)) / 2
                rec_h0 = (int)(x0 * rate)
                rec_h1 = (int)(x1 * rate)
                rec_w0 = (int)((y0 - side) * rate)
                rec_w1 = (int)((y1 - side) * rate)
                sub = img[rec_w0:rec_w1, rec_h0:rec_h1, :]
                # print("switch:%d,%d,%d,%d" % (rec_h0, rec_h1, rec_w0, rec_w1))
                cv.imshow("sub", sub)
                cv.waitKey(0)
                cv.imwrite(res_list[res_index], sub)
            if h / w < 621 / 381:
                rate = w / 381.0
                print(rate)
                side = (621 - (h / rate)) / 2
                rec_h0 = (int)((x0 - side) * rate)
                rec_h1 = (int)((x1 - side) * rate)
                rec_w0 = (int)(y0 * rate)
                rec_w1 = (int)(y1 * rate)
                sub = img[rec_w0:rec_w1, rec_h0:rec_h1, :]
                cv.imshow("sub", sub)
                cv.waitKey(0)
                cv.imwrite(res_list[res_index], sub)
            print(res_list[res_index])
            forecast.forecast(res_list[res_index])
            print(gv.forecast_label[res_list[res_index]])
            self.label.hide()
            self.label_print.show()
            self.hand = False

        if self.auto == True:
            x, y = self.label_auto.get_point()
            img = cv.imread(self.org_path)
            h, w, c = img.shape
            if h / w > 621 / 381:
                rate = h / 621.0
                side = (381 - (w / rate)) / 2
                img_x = (int)(x * rate)
                img_y = (int)((y - side) * rate)
                # print("%d,%d,%d,%d"%(x,y,img_x,img_y))
            else:
                rate = w / 381.0
                side = (621 - (h / rate)) / 2
                img_x = (int)((x - side) * rate)
                img_y = (int)(y * rate)
            pre = box.threshold(box.EPF(box.erode_demo(img)))
            pre = box.erode_demo(pre)
            h, w = pre.shape
            sub = box.box(img, pre, img_x, img_y, (int)(w / 15), (int)(h / 11), h, w)
            cv.imshow("auto", sub)
            cv.imwrite(res_list[res_index], sub)

            print(res_list[res_index])
            forecast.forecast(res_list[res_index])
            print(gv.forecast_label[res_list[res_index]])

            self.label_auto.hide()
            self.label_print.show()
            self.auto = False

    # print("small:%d,%d,%d,%d" % (x0, x1, y0, y1))
"""-----------------------------------------------------------------------------------------------"""
"""’单字浏览‘窗口========"""
class single_Window(QWidget,single_dialog):
    def __init__(self, parent=None):
        super(single_Window, self).__init__()
        self.setupUi(self)
        self.sea = search_Window()
        self.pushButton_2.clicked.connect(self.left)
        self.pushButton_3.clicked.connect(self.right)
        self.pushButton.clicked.connect(self.print_org)
        self.pushButton_4.clicked.connect(self.sea.show)

    def open(self):
        if len(gv.final_label) == 0 or img_list == None:
            self.show_message()
        else:
            for i in gv.final_label.keys():
                final_list.append(i)

            self.display(final_list[final_index])
            self.show()

    def left(self):
        global final_index
        if final_index == 0:
            final_index = len(final_list)-1
            self.display(final_list[final_index])
        else:
            final_index -= 1
            self.display(final_list[final_index])

    def right(self):
        global final_index
        if final_index == len(final_list)-1:
            final_index = 0
            self.display(final_list[final_index])
        else:
            final_index += 1
            self.display(final_list[final_index])

    def show_message(self):
        QMessageBox.information(self, "提示", "\n尚未导入图像\t\n", QMessageBox.Ok)
    def display(self, path):
        # cv.imread(path)
        self.label.setPixmap(QPixmap(""))
        img = QtGui.QPixmap(path).scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(img)
        result = gv.final_label[final_list[final_index]]
        print(result)
        if len(result) ==1:
            self.label_2.setText(gv.ch[str(result[0])])
        if len(result) ==2:
            self.label_2.setText(gv.ch[str(result[0])] + " or " +gv.ch[str(result[1])])
    def print_org(self):
        global res_index
        full_name = final_list[final_index]
        print(full_name)
        sub = full_name.split("\\")
        sub_last = sub[len(sub)-1]
        print(sub_last)
        ext = sub_last.split('.')
        name = sub_last.split('(')
        final_name = name[0] +'.'+ ext[len(ext)-1]
        print(final_name)
        path = os.path.join(gv.rootdir,final_name)
        print(path)
        cv.namedWindow("Original map")
        img = cv.imread(path)
        cv.imshow("Original map",img)
        cv.waitKey(0)
        cv.destroyAllWindows()
"""-----------------------------------------------------------------------------------------------"""
"""’单字查询‘窗口========"""
class search_Window(QWidget,search_dialog):
    def __init__(self, parent=None):
        super(search_Window, self).__init__()
        self.setupUi(self)
        self.same = same_Window()
        self.pushButton.clicked.connect(self.search)

    def show_message(self, title, text):
        QMessageBox.information(self, title, text, QMessageBox.Ok)
    def open(self):
        self.show()
    def search(self):
        if gv.recongnize_flag == False:
            global t_list,t_index
            t_list = []
            t_index = 0
            info = self.textEdit.toPlainText()
            temp_result = gv.get_laber_key(gv.ch, info)
            print(temp_result)
            if temp_result[0] != 'false':
                # print(temp_result)
                for i in gv.final_label.keys():
                    temp = gv.final_label[i]
                    # print(temp)
                    if int(temp_result[0]) == temp[0]:
                        # print(i)
                        t_list.append(i)
                # print(t_list)
                self.same.setWindowTitle(gv.ch[temp_result[0]])
                self.same.open()
            else:
                self.show_message('提示','输入字符不在《勤礼碑》中\n或输入格式不对：\n删除空格等无用字符再尝试')
        else:
            self.show_message('提示','正在进行单字识别，无法查询！')
"""-----------------------------------------------------------------------------------------------"""
"""’单字查询结果显示‘窗口========"""
class same_Window(QWidget,same_scan):
    def __init__(self, parent=None):
        super(same_Window, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.left)
        self.pushButton_2.clicked.connect(self.right)
        self.update()

    def open(self):
        self.display(t_list[t_index])
        self.show()
    def display(self,path):
        self.label.setPixmap(QPixmap(""))
        img = QtGui.QPixmap(path).scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
        self.label.setPixmap(img)

    def left(self):
        global t_index
        if t_index == 0:
            t_index = len(t_list)-1
            self.display(t_list[t_index])
        else:
            t_index -=1
            self.display(t_list[t_index])

    def right(self):
        global t_index
        if t_index == len(t_list) - 1:
            t_index = 0
            self.display(t_list[t_index])
        else:
            t_index += 1
            self.display(t_list[t_index])
    def closeEvent(self, QCloseEvent):
        t_list = []
        t_index = 0
        # self.closeEvent()
"""-----------------------------------------------------------------------------------------------"""
"""’设置‘窗口========"""
class set_Window(QWidget,setting_dialog):
    def __init__(self, parent=None):
        super(set_Window, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.speedup_forecast)
        self.pushButton_2.clicked.connect(self.speedup_final)

    def open(self):
        self.show()

    def show_message(self, title, text):
        QMessageBox.information(self, title, text, QMessageBox.Ok)
    def speedup_final(self):
        flag = gv.re_write_final_label()
        if flag == True:
            self.show_message('成功','完成对文件的优化重写')
        else:
            self.show_message('失败','文件不存在或不存在需要重写内容')
    def speedup_forecast(self):
        flag = gv.re_write_forecast_label()
        if flag == True:
            self.show_message('成功','完成对文件的优化重写')
        else:
            self.show_message('失败','文件不存在或不存在需要重写内容')
"""-----------------------------------------------------------------------------------------------"""
"""’帮助‘窗口========"""
class help_Window(QWidget,help_dialog):
    def __init__(self, parent=None):
        super(help_Window, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.input)
        self.pushButton_2.clicked.connect(self.output)
        self.pushButton_3.clicked.connect(self.cut)
        self.pushButton_4.clicked.connect(self.scan)
        self.pushButton_5.clicked.connect(self.single)
        self.pushButton_6.clicked.connect(self.set)
        self.label_2.setText('《颜勤礼碑》')
        self.label.setText('  ·唐颜真卿撰文书丹，自署立于大历十四年(779年)。'
                           '楷书，碑文一通。残石175×90×22厘米。'
                           '碑四面环刻，存书三面。碑阳19行，碑阴20行，行38字。左侧5行，行37字。 '
                           '右侧上半宋人刻“忽惊列岫晓来逼，朔雪洗尽烟岚昏”十四字，下刻民国宋伯鲁题跋。'
                           '现存西安碑林，北京故宫博物院藏初拓本。《颜勤礼碑》在拙重中见挺拔雄肆之气概，'
                           '《麻姑仙坛记》则在宽博中见空灵洞达之韵度，堪称颜楷的双峰并峙。'
                           '\n'
                           '  ·此碑全称《唐故秘书省著作郎夔州都督府长史上护军颜君神道碑》。'
                           '颜勤礼乃颜真卿曾祖父，颜真卿撰并刊立此碑时，年71岁。'
                           '此碑在欧阳修《集古录》中曾有记载，但清《金石萃编》等书却未著录，颜勤礼碑可见此碑在北宋时尚为人知。'
                           '元明时被埋入土中， 至民国年间才重新发现。 据宋伯鲁1923年的题跋称：此碑1922年10月曾由何梦庚得之于西安旧藩廨库堂后土中，'
                           '时碑虽已中断，但上下都完好，惟其铭文并立石年月，因宋时作基址而磨灭。初出土拓本，'
                           '“长老之口故”之“故”字，当断处有断线纹，但不损笔画。其后“故”字下泐。首行“碑”字右竖笔未损。'
                           '\n'
                           '  ·此碑是颜真卿晚年精品，已完全脱去了初唐楷法的体态。此碑结字端庄，宽润疏朗，气势雄强，'
                           '骨架开阔，方形外拓，横细竖粗非常鲜明，方圆转折的笔法清晰。由于入土较早，残剥损毁少，'
                           '又未经后人修刻剔剜，所以能比较准确地体现颜书宽绰、厚重、挺拔、坚韧的风神。他的楷书一反初'
                           '唐书风，行以篆籀之笔，化瘦硬为丰腴雄浑，结体宽博而气势恢宏，骨力遒劲而气概凛然，'
                           '这种风格也体现了大唐帝国繁盛的风度，并与他高尚的人格契合，是书法美与人格美完美结合'
                           '的典例。')


    def open(self):
        self.show()
    def input(self):
        self.label_2.setText('关于导入图片')
        self.label.setText('   请首先将待处理的碑帖文件放入一个文件夹内，并确保该文件夹内无其他无关图像文件\n'
                           '   之后选择文件所在文件夹，单击确定即可完成图像导入')
    def output(self):
        self.label_2.setText('关于设置输出目录')
        self.label.setText('   此步可以省略，如果有特殊的输出要求，'
                           '选择输出文件夹，并单击确定即可完成输出目录的设置\n'
                           '   请确保输出文件夹内无无关的图像文件！'
                           '否则可能影响图像的识别工作！' )
    def cut(self):
        self.label_2.setText('关于碑帖裁切')
        self.label.setText('   开始此步前，请确保成功导入图像\n'
                           '单击开始进行切割，请再切割完成后在进行单字识别！\n'
                           '进行完成单子识别后，请进入结果查看，进行最终结果的查看与确认！\n'
                           '细节如下：\n'
                           '   单字切割中使用纵横积分法对图像文件进行切割，并对勤礼碑贴做了适应性优化。使得切割效果更佳，'
                           '但并不排除会出现错误，再“查看结果”按钮出可以进行修改\n'
                           '   单字识别中，使用了深度神经网络Alex net作为训练模型，由于现存《勤礼碑》残破较多，因此'
                           '识别结果受白块的影响较大。您可以再查看结果中对结果进行修改与确认\n'
                           '   查看结果 界面中显示了对切割完成后的单字的识别结果，如果正确不需要做任何操作，直接点击下一个'
                           '或者上一个按钮即可。如果图像切割不正确，您可以点击响应按钮进行修改其中\n'
                           '     ·手动切割，会保留您选择的框内图像\n'
                           '     ·自动切割，使用区域膨胀算法，为保证切割效果，请尽量点击单字的中心位置！\n'
                           '        ※注意：不同的切割方式可能对单子识别的结果造成不同的影响！'
                           '        为保证最终的结果，再查看界面重新对结果进行查看或修改\n'
                           '   若切割图像属于无效的白色块图像，您可以点击删除按钮删除此图像。\n'
                           )
    def scan(self):
        self.label_2.setText('关于浏览碑帖')
        self.label.setText('   请确保图像文件夹已经导入完成，关于细节您可以参考‘关于导入图片’按钮中的相关信息'
                           '   翻页直接单击下一张或上一张即可更换图片。\n'
                           '    翻页可以循环翻页，比如当浏览到最后一个碑文时，点击下一张会回到第一张图像，反之亦然。' )
    def single(self):
        self.label_2.setText('关于查找单字')
        self.label.setText('   进行此步前，请先进行单字识别。\n'
                           '   该窗口会显示单字图像、改字为什么汉字\n'
                           '   如果您需要到原碑帖中查看，直接点击查看原图即可。\n'
                           '    ·关于单字查询：\n'
                           '    输入您要查询的单字，系统将会显示以识别的改字的图像。您可以点击相关按钮更换翻看结果。\n'
                           '    ※注意：为保证程序不异常退出，进行单字识别的时候，不可以进行单字查询\n' )
    def set(self):
        self.label_2.setText('关于 设置')
        self.label.setText('    设置界面中，存在两个按钮'
                           '系统对于单字识别、修改的信息保存在了文本文件中，运行过久之后可能会造成系统启动过慢。\n'
                           '这两个功能就是为了解决此状况而设的，因此您发现系统启动过慢时，可以单击这两个按钮来加速系统的载入速度。' )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    about = AboutWindow()
    scan = Scan_rubbing()
    cut = CutWindow()
    single = single_Window()
    set = set_Window()
    help = help_Window()

    main.show()
    main.pushButton_6.clicked.connect(about.open)
    main.pushButton_5.clicked.connect(single.open)
    main.pushButton_3.clicked.connect(main.input_img)
    main.pushButton_4.clicked.connect(main.set_output)
    main.pushButton_2.clicked.connect(scan.open)
    main.pushButton.clicked.connect(cut.open)
    main.pushButton_7.clicked.connect(set.open)
    main.pushButton_8.clicked.connect(help.open)

    sys.exit(app.exec_())

