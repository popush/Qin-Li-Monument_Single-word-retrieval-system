# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
import numpy as np
import os
import codecs

# "hanyifanti.ttf","shutifangyanti.ttf", "5.ttf"
Fonts = ["7.ttf", "8.ttf", "9.TTF", "6.ttf", "4.ttf", "3.ttf", "2.TTF", "1.TTF"]
output_dir = 'C:\\graduation_project\\example\\'


# 噪点增加
def add_noise(img):
    temp = img
    for i in range(50):  # 添加噪声
        temp_x = np.random.randint(0, temp.shape[0] - 1)
        temp_y = np.random.randint(0, temp.shape[1] - 1)
        for i in range(np.random.randint(0, 10)):
            for j in range(np.random.randint(0, 10)):
                temp[temp_x - i][temp_y - j] = 255
    return temp

def add_broke(img):
    temp = img
    i=0
    while i < 25:
        temp_x = np.random.randint(0, temp.shape[0] - 1)
        temp_y = np.random.randint(0, temp.shape[1] - 1)
        if temp[temp_x][temp_y][0] == 255:
            for i in range(np.random.randint(0, 25)):
                for j in range(np.random.randint(0, 25)):
                    temp[temp_x - i][temp_y - j][0] = 0
                    temp[temp_x - i][temp_y - j][1] = 0
                    temp[temp_x - i][temp_y - j][2] = 0
        i+=1
    return temp



# 适当腐蚀
def add_erode(img, i):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (i, i))
    img1 = cv.erode(img, kernel)
    return img1


# 适当膨胀
def add_dilate(img, i):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (i, i))
    img1 = cv.dilate(img, kernel)
    return img1


if __name__ == "__main__":

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # length = 0x9fa6 - 0x4e00

    f = codecs.open('chinese_labels.txt', 'r', 'utf-8')
    content = f.readlines()

    f = codecs.open(r'C:\graduation_project\TRAIN_INFO.txt', 'w')
    fc = codecs.open(r'C:\graduation_project\LABER_HELP.txt', 'w', 'utf-8')

    count = 0
    laber_count = 0
    for line in content:

        fc.write(str(laber_count) + " " + line)

        line = line.rstrip('\n')
        if len(line) == 0:
            continue
        print(line)

        for j in range(len(Fonts)):
            # cv读取图片
            img = np.zeros((150, 150, 3), dtype=np.uint8)
            cvimg = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # cv和PIL中颜色的hex码的储存顺序不同
            pilimg = Image.fromarray(cvimg)

            # PIL图片上打印汉字
            draw = ImageDraw.Draw(pilimg)  # 图片上打印

            font = ImageFont.truetype(Fonts[j], 150, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
            draw.text((0, 0), line, (255, 255, 255), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

            # PIL图片转cv 图片
            cvcharimg = cv.cvtColor(np.array(pilimg), cv.COLOR_RGB2BGR)

            cvcharimg = cv.resize(cvcharimg, (227, 227), interpolation=cv.INTER_CUBIC)

            mean_list = cv.mean(cvcharimg)
            if mean_list[0] != 0:

                h, w, c = cvcharimg.shape
                savePath = (r"C:\graduation_project\example\\TRAIN_" + str(count) + ".jpg")
                # print(line+"\\\\"+str(j))
                # cvcharimg = cut_ch(cvcharimg)
                cv.imencode('.jpg', cvcharimg)[1].tofile(savePath)
                f.write("TRAIN_" + str(count) + ".jpg" + " " + str(laber_count) + "\n")
                count += 1

                savePath = (r"C:\graduation_project\example\\TRAIN_" + str(count) + ".jpg")

                noised = add_noise(cvcharimg)
                cv.imencode('.jpg', noised)[1].tofile(savePath)
                f.write("TRAIN_" + str(count) + ".jpg" + " " + str(laber_count) + "\n")
                count += 1

                savePath = (r"C:\graduation_project\example\\TRAIN_" + str(count) + ".jpg")
                broken = add_broke(noised)
                cv.imencode('.jpg', broken)[1].tofile(savePath)
                f.write("TRAIN_" + str(count) + ".jpg" + " " + str(laber_count) + "\n")
                count += 1


                for l in range(1, 12, 2):
                    savePath = (r"C:\graduation_project\example\\TRAIN_" + str(count) + ".jpg")

                    # print(line + "\\\\" + str(j))
                    eroded = add_erode(broken, l)
                    cv.imencode('.jpg', eroded)[1].tofile(savePath)
                    f.write("TRAIN_" + str(count) + ".jpg" + " " + str(laber_count) + "\n")
                    count += 1

                for l in range(1, 9, 2):
                    savePath = (r"C:\graduation_project\example\\TRAIN_" + str(count) + ".jpg")

                    # print(line + "\\\\" + str(j))
                    dilated = add_dilate(broken, l)
                    cv.imencode('.jpg', dilated)[1].tofile(savePath)
                    f.write("TRAIN_" + str(count) + ".jpg" + " " + str(laber_count) + "\n")
                    count += 1

                for m in range(0, 11, 5):
                    for l in range(0, 11, 5):
                        savePath = (r"C:\graduation_project\example\\TRAIN_" + str(count) + ".jpg")

                        moved = np.zeros((227, 227, 3), dtype=np.uint8)
                        moved[m:217 + m, l:217 + l] = cvcharimg[l:217 + l, m:217 + m]
                        cv.imencode('.jpg', moved)[1].tofile(savePath)
                        f.write("TRAIN_" + str(count) + ".jpg" + " " + str(laber_count) + "\n")
                        count += 1
        laber_count += 1
        print(laber_count)
        # print("%d,%d"%(k,l))
    f.close()
    fc.close()
    cv.waitKey(0)
    cv.destroyAllWindows()
