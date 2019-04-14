import threading
import queue, time
from Graduition_projict import  golbal
import cv2 as cv
import numpy as np
import imghdr
import os
import heapq
import queue
from multiprocessing import cpu_count
import matplotlib.pyplot as plt
from Alex_Net import sus_one_pic as forecast

Img_type = ['png', 'jpeg', 'bmp', 'pbm', 'pgm', 'ppm', 'rast', 'tiff', 'exr']
q = queue.Queue(maxsize=10)

empty = threading.Semaphore(5)  # 创建信号量empty表示可以防止产品的位置，并赋初值为10

full = threading.Semaphore(0)  # 被占满的空（物品）的信号量

mutex = threading.Event()  # 生产者与消费者互斥信号量

mutex1 = threading.Event()  # 消费者之间互斥信号量

file = queue.Queue(11)

cpu_count = cpu_count()
golbal.end_flag = False

# golbal.rootdir = 'C:\\graduation_project'  # 处理内容的放置位置
#
# golbal.output_dir = 'C:\\graduation_project'  # 输出内容的放置位置
# lock=threading.Lock();
golbal.id1 = 0
golbal.id2 = 0

print_count = 0

mutex.set()  # 设标志为True
mutex1.set()

"""--------------------------函数定义--------------------------------"""

"""返回list中最小的两个数组↓↓↓↓↓↓"""
def get_min(list_px):
    min_index_list = list(map(list_px.index, heapq.nsmallest(2, list_px)))
    return min_index_list

"""将多余的列切割线清除↓↓↓↓↓↓"""
def cut_error_col(cut, weight):
    sum = 0
    for i in range(1, len(cut)):
        sum += (cut[i] - cut[i - 1])
    average = int(sum / len(cut))
    i = 0
    while i < len(cut) - 1:
        if (cut[i] - cut[i - 1]) < average and (cut[i + 1] - cut[i]) < average:
            del cut[i + 1]
            i -= 1
        i += 1
    i = 1
    cut.sort()
    while i < len(cut):
        if cut[i] - cut[i - 1] < weight:
            del cut[i]
        i += 1
    return cut

"""将多余的行切割线清除,对未切割的部分添加处理↓↓↓↓↓↓"""
def cut_error_row(cut, weight, high, wide):
    """对于双子/多字粘连的情况进行分割↓↓↓↓↓↓"""
    cut.sort()
    if len(cut) > 0:
        if cut[0] > 20:
            cut.append(2)
        # if high-cut[len(cut)-1]<10:
    cut.append(high - 5)
    cut.append(high - 6)
    cut.sort()
    # print(cut)
    range_single = (int)(high / 5)  # 均分为5份
    cut_help = (int)(high / 20)  # 切割的幅度
    x = 0
    while x < len(cut) - 1:
        for y in range(0, 6):
            if cut[x] > (y * range_single + cut_help) and cut[x] < ((y + 1) * range_single - cut_help):
                del cut[x]
                break
        x += 1
    i = 1
    while i < len(cut) - 1:
        if (cut[i + 1] - cut[i]) + (cut[i] - cut[i - 1]) < weight:
            del cut[i + 1]
        else:
            i += 1
    x = 0
    while x < len(cut) - 1:
        for y in range(0, 6):
            if cut[x] > (y * range_single + cut_help) and cut[x] < ((y + 1) * range_single - cut_help):
                del cut[x]
                break
        x += 1
    if cut[0] < weight:
        cut[0] = 2
    if cut[1] < weight:
        cut[1] = 2
    if high - cut[len(cut) - 1] < weight:
        cut[len(cut) - 1] = high - 2
    if high - cut[len(cut) - 2] < weight:
        cut[len(cut) - 2] = high - 2
    # print("final:")
    # print(cut)
    return cut

"""确保打开文件正确↓↓↓↓↓↓"""
def is_img(path):
    path = path.lower()
    type = imghdr.what(path)
    if type in Img_type:
        return True
    else:
        return False

"""均值偏移滤波↓↓↓↓"""
def EPF(image):
    dst = cv.pyrMeanShiftFiltering(image, 10, 100)
    #    cv.imshow("junzhi - qianyi", dst)
    return dst

"""阈值化↓↓↓↓↓↓↓↓↓"""
def threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # print("value：%s"%ret)
    # cv.imshow("OTSU",binary)
    return binary

"""腐蚀膨胀算法↓↓↓↓↓↓"""
def erode_demo(image):
    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (3, 3))
    dst = cv.erode(image, kernel)
    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (5, 5))
    dst = cv.dilate(dst, kernel)
    # cv.imshow("dilate", dst)
    return dst

"""泛洪填充，用于处理边缘留白↓↓↓↓↓↓"""
def flood_fill(img, edge_size):
    copyimg = img.copy()
    h, w = img.shape[:2]
    # print("weight : %s, height : %s" % (w, h))
    mask = np.zeros([h + 2, w + 2], np.uint8)
    # 遍历高度在0~3edge_size\所有宽度的点,消除边框
    # edge_size = 5
    for i in range(w):
        for j in range(0, edge_size):
            if (img[j, i] != 0):
                cv.floodFill(copyimg, mask, (i, j), (0, 0, 0), (0, 0, 0), (0, 0, 0), cv.FLOODFILL_FIXED_RANGE)
    for i in range(w):
        for j in range(h - edge_size, h):
            if (img[j, i] != 0):
                cv.floodFill(copyimg, mask, (i, j), (0, 0, 0), (0, 0, 0), (0, 0, 0), cv.FLOODFILL_FIXED_RANGE)
    for j in range(h):
        for i in range(0, edge_size):
            if (img[j, i] != 0):
                cv.floodFill(copyimg, mask, (i, j), (0, 0, 0), (0, 0, 0), (0, 0, 0), cv.FLOODFILL_FIXED_RANGE)
    for j in range(h):
        for i in range(w - edge_size, w):
            if (img[j, i] != 0):
                cv.floodFill(copyimg, mask, (i, j), (0, 0, 0), (0, 0, 0), (0, 0, 0), cv.FLOODFILL_FIXED_RANGE)
    # cv.imshow("fill",copyimg)
    return copyimg

"""进行列切割，返回图片↓↓↓↓↓↓"""
def draw_col(img, line):
    # print(x)
    h, w = img.shape
    for i in range(h):
        for j in range(len(line)):
            img[i, line[j]] = 255
    # cv.imshow("zong", img)
    return img

"""进行列切割，返回图片↓↓↓↓↓↓"""
def draw_row(img, line, begin, done):
    h2, w2 = img.shape
    for i in range(len(line)):
        for j in range(done - begin):
            for k in range(w2):
                img[line[i], j + begin] = 255
    # cv.imshow("heng", img)
    return img

"""============||||||||========================进行行切割，返回图片↓↓↓↓↓↓"""
def analise_row(img, line, row_info):
    h1, w1 = img.shape
    row_cuted = []
    for i in range(len(line) - 1):
        h_px = []
        col_index = []
        zone = [0, 0, 0, 0]
        min_size = int(h1 / 10)
        final_row = []
        begin = line[i]
        done = line[i + 1]  # begin = left;done = right
        for row in range(h1):  # 纵向遍历
            x = 0
            for col in range(done - begin):
                if img[row, col + begin] == 255:
                    x += 1
            h_px.append(x)  # """得到一列内的行积分"""
        for j in range(1, len(h_px) - 1):
            h_px[i] = int(h_px[i + 1] + h_px[i] + h_px[i - 1]) / 3  # 对积分进行处理

        # plt.plot(h_px)
        # plt.title(i,fontsize=24)
        # plt.xlabel("coordinate",fontsize=14)
        # plt.ylabel("number",fontsize=14)
        # plt.tick_params(axis='both',labelsize=14)
        # plt.show('hist')
        # print(h_px)


        for i in range(1, len(h_px) - 1):
            if h_px[i] < 10:
                if h_px[i - 1] >= 10:
                    col_index.append(i)
                if h_px[i + 1] >= 10:
                    col_index.append(i)
        # print(col_index)
        wide = done - begin
        i = 0
        col_index.append(2)
        col_index.append(h1 - 2)
        col_index.sort()
        while i < len(col_index) - 1:

            length = col_index[i + 1] - col_index[i]
            if length / wide > 1.5 and length / wide < 2.3:
                # print("%f"%(length / wide))
                temp_list = h_px[col_index[i] + (int)(length * 0.45):col_index[i + 1] - (int)(length * 0.45)]
                min_index_list = get_min(temp_list)
                if len(min_index_list) == 2:
                    col_index.append(col_index[i] + (int)(length * 0.45) + min_index_list[0])
                    col_index.append(col_index[i] + (int)(length * 0.45) + min_index_list[1])
                else:
                    if len(col_index) == 1:
                        col_index.append(col_index[i] + (int)(length * 0.45) + min_index_list[0])

            if length / wide > 2.3 and length / wide < 3.3:
                temp_list = h_px[col_index[i] + (int)(length * 0.30):col_index[i + 1] - (int)(length * 0.64)]
                min_index_list = get_min(temp_list)
                if len(min_index_list) == 2:
                    col_index.append(col_index[i] + (int)(length * 0.30) + min_index_list[0])
                    col_index.append(col_index[i] + (int)(length * 0.30) + min_index_list[1])
                else:
                    if len(col_index) == 1:
                        col_index.append(col_index[i] + (int)(length * 0.30) + min_index_list[0])

                temp_list = h_px[col_index[i] + (int)(length * 0.63):col_index[i + 1] - (int)(length * 0.30)]
                min_index_list = get_min(temp_list)
                if len(min_index_list) == 2:
                    col_index.append(col_index[i] + (int)(length * 0.63) + min_index_list[0])
                    col_index.append(col_index[i] + (int)(length * 0.63) + min_index_list[1])
                else:
                    if len(col_index) == 1:
                        col_index.append(col_index[i] + (int)(length * 0.63) + min_index_list[0])

            if length / wide > 3.3 and length / wide < 4.3:
                temp_list = h_px[col_index[i] + (int)(length * 0.23):col_index[i + 1] - (int)(length * 0.73)]
                min_index_list = get_min(temp_list)
                if len(min_index_list) == 2:
                    col_index.append(col_index[i] + (int)(length * 0.23) + min_index_list[0])
                    col_index.append(col_index[i] + (int)(length * 0.23) + min_index_list[1])
                else:
                    if len(col_index) == 1:
                        col_index.append(col_index[i] + (int)(length * 0.23) + min_index_list[0])

                temp_list = h_px[col_index[i] + (int)(length * 0.48):col_index[i + 1] - (int)(length * 0.52)]
                min_index_list = get_min(temp_list)
                if len(min_index_list) == 2:
                    col_index.append(col_index[i] + (int)(length * 0.48) + min_index_list[0])
                    col_index.append(col_index[i] + (int)(length * 0.48) + min_index_list[1])
                else:
                    if len(col_index) == 1:
                        col_index.append(col_index[i] + (int)(length * 0.48) + min_index_list[0])

                temp_list = h_px[col_index[i] + (int)(length * 0.73):col_index[i + 1] - (int)(length * 0.23)]
                min_index_list = get_min(temp_list)
                if len(min_index_list) == 2:
                    col_index.append(col_index[i] + (int)(length * 0.73) + min_index_list[0])
                    col_index.append(col_index[i] + (int)(length * 0.73) + min_index_list[1])
                else:
                    if len(col_index) == 1:
                        col_index.append(col_index[i] + (int)(length * 0.73) + min_index_list[0])
            i += 1
        final_row = cut_error_row(col_index, (int)(min_size * 1.5), h1, done - begin)  # 1.5倍数别动了
        row_info.append(final_row)
        row_cuted.append(draw_row(img, final_row, begin, done))
        h_px = []
        final_row = []
    # print(row_info)
    return row_cuted[len(row_cuted) - 1]

"""进行列投影分析，返回的是可切割出列的横坐标↓↓↓↓↓↓"""
def analise_col(img):
    global col_info
    h, w = img.shape
    list_px = []
    trough_index = []
    final_trough = []
    for col in range(w):  # 纵向遍历
        x = 0
        for row in range(h):
            if img[row, col] == 255:
                x += 1
        list_px.append(x)

    for i in range(1, len(list_px) - 1):
        list_px[i] = int(list_px[i + 1] + list_px[i] + list_px[i - 1]) / 3
    # plt.plot(list_px)
    # plt.title("lie qie ge",fontsize=24)
    # plt.xlabel("coordinate",fontsize=14)
    # plt.ylabel("number",fontsize=14)
    # plt.tick_params(axis='both',labelsize=14)
    # plt.show('hist')
    left = 0
    right = 0
    for i in range(1, len(list_px) - 1):
        if list_px[i] == 0:
            if list_px[i - 1] != 0:
                if i > w / 2:
                    if i < w - (w / 4):
                        right = 1
                elif i > w / 4:
                    left = 1
                trough_index.append(i)
            if list_px[i + 1] != 0:
                trough_index.append(i)
    if left == 0:
        left_list = list_px[int(w / 4): int(w / 2)]
        min_index_list = get_min(left_list)
        trough_index.append(int(w / 4) + min_index_list[0])
        trough_index.append(int(w / 4) + min_index_list[1])
    if right == 0:
        right_list = list_px[int(w / 2): int(w - (w / 4))]
        min_index_list = get_min(right_list)
        trough_index.append(int(w / 2) + min_index_list[0])
        trough_index.append(int(w / 2) + min_index_list[1])
    final_trough = cut_error_col(trough_index, int(w / 6))
    col_info = final_trough
    # print(col_info)
    return final_trough

"""对一张图片进行处理↓↓↓↓↓↓"""
def adress(img_name, img_path):
    row_info = []  # 捕获图片要切割的列的位置信息
    src = cv.imread(img_path)
    pre = threshold(EPF(erode_demo(src)))

    # cv.imwrite(r'C:\Users\Administrator\Desktop\bishe\img\img443_threshold.jpg', pre)

    col_info = analise_col(flood_fill(pre, 5))  # 返回切割的列的信息
    col_cut = draw_col(pre, col_info)  # 返回切割好的图片


    # cv.imwrite(r'C:\Users\Administrator\Desktop\bishe\img\img122_lie_youhua.jpg', col_cut)
    # cv.imshow('1',col_cut)
    # cv.waitKey(0)

    cut = analise_row(col_cut, col_info, row_info)
    if not os.path.exists(golbal.output_dir + "\\one\\"):
        os.mkdir(golbal.output_dir + "\\one\\")
    cv.imwrite(golbal.output_dir + "\\one\\" + img_name, cut)
    if not os.path.exists(golbal.output_dir + "\\single\\"):
        os.mkdir(golbal.output_dir + "\\single\\")
    if not os.path.exists(golbal.output_dir + "\\pre\\"):
        os.mkdir(golbal.output_dir + "\\pre\\")
    #



    for i in range(len(col_info) - 1):  # 遍历列
        row_temp = row_info[i]
        # print(row_temp)
        for j in range(len(row_temp) - 1):  # 遍历行

            if row_temp[j] == row_temp[j + 1] or col_info[i] == col_info[i + 1]:  # 消除相同切割线
                # print("countinue")
                continue
            else:

                if (col_info[i + 1] - col_info[i]) / (row_temp[j + 1] - row_temp[j]) < 2:  # 消除字之间的分割线
                    # print("row_temp:%s,row_temp:%s    col_:%s,col_%s" % (row_temp[j], row_temp[j + 1], col_info[i], col_info[i + 1]))
                    temp_ensure = pre[row_temp[j]:row_temp[j + 1], col_info[i]:col_info[i + 1]]
                    mean_list = cv.mean(flood_fill(temp_ensure, 2))
                    if mean_list[0] > 10:
                        temp = src[row_temp[j]-1:row_temp[j + 1], col_info[i]-1:col_info[i + 1]]
                        temp_pre = pre[row_temp[j]-1:row_temp[j + 1], col_info[i]-1:col_info[i + 1]]
                        temp_pre = cv.merge([temp_pre, temp_pre, temp_pre])
                        left_head = "(%d,%d)" % (row_temp[j], col_info[i])
                        pure_name = img_name.split('.')
                        # cv.imshow(golbal.output_dir + "\\single\\" + img_name + name_add, temp)
                        # cv.waitKey(1)
                        temp_path = golbal.output_dir + "\\single\\" + pure_name[0] + left_head + "." + pure_name[1]
                        # ch_index = forecast.forecast(temp_path)
                        cv.imwrite(temp_path, temp)
                        cv.imwrite(golbal.output_dir + "\\pre\\" + pure_name[0] + left_head + "." + pure_name[1], temp_pre)
    # print("使用了%fs" % ((t2 - t1) / cv.getTickFrequency()))

                        # golbal.forecast_label[golbal.output_dir + "\\single\\" + pure_name[0] + left_head + "." + pure_name[1]] =str(ch_index)
    golbal.img_cut.setdefault(img_path, []).append(col_info)
    golbal.img_cut.setdefault(img_path, []).append(row_info)
    # print(golbal.img_cut.get(img_path))

# 消费者
"""读取文件名到待处理队列中↓↓↓↓↓↓"""
def consumer(id):
    # global empty, mutex, lock, full, file, golbal.id2, golbal.end_flag
    global empty, mutex, lock, full, file
    print('处理线程' + id + '开始工作')
    while True:
        mutex1.clear()
        full.acquire()
        mutex.clear()
        if not file.empty():
            img_name = file.get()
            # print("取出%s"%(img_name))
            # do something
            golbal.id2 += 1
            mutex.set()
            empty.release()
            mutex1.set()

            img_path = golbal.rootdir + "\\" + img_name
            t1 = cv.getTickCount()
            adress(img_name, img_path)
            t2 = cv.getTickCount()
            print("处理文件 " + img_name + "使用了 %.3fs" % ((t2 - t1) / cv.getTickFrequency()))

            # time.sleep(0.1)
        if golbal.end_flag == True and file.empty():
            break
    print_end()




# 生产者
"""将队列中的文件进行处理↓↓↓↓↓↓"""
def producer():
    # global empty, mutex, lock, full, file, golbal.id1, golbal.end_flag
    global empty, mutex, lock, full, file
    dir_list = os.listdir(golbal.rootdir)  # 列出文件夹下所有的目录与文件
    i = 0
    length = len(dir_list)
    while i < length:
        path = os.path.join(golbal.rootdir, dir_list[i])
        if os.path.isfile(path):
            if (is_img(path)):
                empty.acquire()
                mutex.clear()
                file.put(dir_list[i])
                mutex.set()
                full.release()
                golbal.id1 += 1
        i += 1
    # print("i:%d     producter:%d" % (i, golbal.id1))
    golbal.end_flag = True

def print_end():
    global print_count
    print_count += 1
    if print_count == cpu_count:
        print("+++++++end++++++")

"""------------------------------主函数--------------------------------"""
def cut_begin():
    print('**======开始处理======**')
    p = threading.Thread(target=producer)
    p.start()
    for i in range(0, cpu_count):
        temp = threading.Thread(target=consumer, args=("consumer---" + str(i),))
        temp.start()
        # print(i)


