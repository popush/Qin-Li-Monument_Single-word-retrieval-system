from Graduition_projict import thread1 as th
from Graduition_projict import put_training_dataset as ptd
import os
import numpy as np
import cv2 as cv
import codecs

rootdir = r"C:\graduation_project\颜勤礼碑单字版"
out = r"C:\graduation_project\checking"




def cv_imread(file_path):
    cv_img = cv.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img


if __name__ == "__main__":
    dir_list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    i = 0
    count = 0
    length = len(dir_list)

    if not os.path.exists(out):
        os.mkdir(out)

    ch = {}

    f = open('C:\graduation_project\ORG_INFO.txt','w')
    fc = codecs.open('C:\graduation_project\LABER_HELP.txt', 'r', 'utf-8')

    # content.split(' ')
    for line in fc.readlines():
        linestr = line.strip()
        linestrlist = linestr.split(" ")
        ch[linestrlist[1]]=linestrlist[0]
    print(ch)

    while i < length:
        path = os.path.join(rootdir, dir_list[i])
        file_name = dir_list[i][4:5]
        # print(file_name)
        if os.path.isfile(path):
            if (th.is_img(path)):
                # print(rootdir+"\\"+dir_list[i])
                src = cv_imread(u"" + rootdir + "\\" + dir_list[i])
                pre = th.threshold(th.EPF(th.erode_demo(src)))
                pre = cv.resize(pre, (227, 227), cv.INTER_AREA)
                pre = cv.merge([pre, pre, pre])

                savePath = out + "\\" + "ORING_" + str(count) + ".jpg"
                print(savePath)
                cv.imencode('.jpg', pre)[1].tofile(savePath)
                print(file_name)
                print(ch.get(file_name))
                f.write("ORING_" + str(count) + ".jpg" + " " + str(ch.get(file_name)) + "\n")
                count += 1

        i += 1
    f.close()
