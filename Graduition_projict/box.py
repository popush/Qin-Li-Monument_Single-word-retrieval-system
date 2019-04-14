"""--------------------------库及全局变量--------------------------------"""
import threading
import queue, time
import cv2 as cv
import scipy.signal as signal
import numpy as np
# import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
import imghdr
import os
import heapq
import queue

output_dir = 'C:\\graduation_project'


def erode_demo(image):
    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (3, 3))
    dst = cv.erode(image, kernel)
    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (5, 5))
    dst = cv.dilate(dst, kernel)
    # cv.imshow("dilate", dst)
    return dst


def EPF(image):
    dst = cv.pyrMeanShiftFiltering(image, 10, 100)
    #    cv.imshow("junzhi - qianyi", dst)
    return dst


def threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # print("value：%s"%ret)
    # cv.imshow("OTSU",binary)
    return binary


# def threshold(image):
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#     dst = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,
#                                (int)(2 * (gray.shape[0] / 50) + 1), 25)
#     return dst


def box(src, img, x, y, org, limit, high, wide):#src = 源文件、img=处理后的图片
    top = org
    bot = org
    left = org
    right = org
    bot1 = right1 = org
    top = y - top
    bot = y + bot
    left = x - left
    right = x + right

    # src[top, left:right] = (0, 255, 255)
    # src[bot, left:right] = (0, 255, 255)
    # src[top:bot, left] = (0, 255, 255)
    # src[top:bot, right] = (0, 255, 255)
    # cv.imshow(output_dir + "\\test\\", src)
    # cv.imwrite(r'C:\Users\Administrator\Desktop\bishe\img\img116_box_1.jpg', src)

    j = 0
    while j < limit:
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        w = right - left
        i = 0
        while i < w and i + left < wide:
            if img[top, i + left] == 255:
                sum1 = sum1 + 1
            if img[bot, i + left] == 255:
                sum2 = sum2 + 1
            i += 1
        # print("top11111111:" + str(top))
        h1 = bot - top
        i = 0
        while i < h1 and i + top < high:
            if img[i + top, left] == 255:
                sum3 = sum3 + 1
            if img[i + top, right] == 255:
                sum4 = sum4 + 1
            i += 1
        # print("top:" + str(top))
        # print("bot:" + str(bot))
        # print("left:" + str(left))
        # print("right:" + str(right))
        # print("================")
        if sum1 != 0:
            if top > 1:
                top = top - 1
        if sum2 != 0:
            if bot < high - 1:
                bot = bot + 1
        if sum3 != 0:
            if left > 1:
                left = left - 1
        if sum4 != 0:
            if right < wide - 1:
                right = right + 1
        if sum1 == 0 and sum2 == 0 and sum3 == 0 and sum4 == 0:
            # print(j)
            break
        j += 1
    # src[top, left:right] = (0, 255, 0)
    # src[bot, left:right] = (0, 255, 0)
    # src[top:bot, left] = (0, 255, 0)
    # src[top:bot, right] = (0, 255, 0)
    # cv.imshow(output_dir + "\\test\\" + str(j), src)
    # cv.imshow(output_dir + "\\single\\" + str(j), src)
    # cv.imwrite(r'C:\Users\Administrator\Desktop\bishe\img\img116_box_2.jpg', src)

    sc = src[top:bot+1,left:right+1,:]#single_channel

    # im = cv.merge([sc,sc,sc])  #将图片保存成为三通道rgb图像
    # cv.imshow("sc",sc)
    # cv.imwrite("C:\graduation_project\\test.jpg",im)
    return sc



#
# src = cv.imread("C:\graduation_project\img116.jpg")
# # cv.namedWindow("origin", cv.WINDOW_AUTOSIZE)
# cv.imshow("origin", src)
# t1 = cv.getTickCount()
# pre = threshold(EPF(erode_demo(src)))
# pre = erode_demo(pre)
# h, w = pre.shape
# box(src, pre, 75, 70, (int)(w / 15), (int)(h / 11), h, w)
# cv.imshow("pre", pre)
# cv.waitKey(0)
