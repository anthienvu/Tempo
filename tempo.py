#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 21:39:05 2020

@author: trungminh
"""


import face_recognition
import cv2
from PIL import Image
import matplotlib.patches as patches
from IPython.display import clear_output
from matplotlib.pyplot import imshow
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from datetime import datetime
import time

from skimage.measure import compare_ssim
import pyscreenshot as ImageGrab
import imutils


def img_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized

    
def img_crop(image):
    face_locations = face_recognition.face_locations(image)
    if face_locations:     #  prevent manipulation of null variable
        top, right, bottom, left = face_locations[0]

        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        image = image[top:bottom, left:right]
    return image
    
def screen_diff(imageA, imageB):
    grayA = cv2.cvtColor(np.float32(imageA), cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(np.float32(imageB), cv2.COLOR_BGR2GRAY)
        
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    print("SSIM Screen: {}".format(score))
    return score

def face_diff(imageA, imageB):
#     max_w, max_h = None, None
#     if imageA.shape[:2] != imageB.shape[:2]:
#         max_w = max(imageA.shape[0], imageB.shape[0])
#         max_h = max(imageA.shape[1], imageB.shape[1])
    
#     # convert the images to grayscale
#     if max_w or max_h:
#         grayA = cv2.cvtColor(
#             imutils.resize(imageA, width=max_w, height=max_h), cv2.COLOR_BGR2GRAY)
#         grayB = cv2.cvtColor(
#             imutils.resize(imageB, width=max_w, height=max_h), cv2.COLOR_BGR2GRAY)
#         if grayA.shape != grayB.shape:
#             gray_max_w = max(grayA.shape[0], grayB.shape[0])
#             gray_max_h = max(grayA.shape[1], grayB.shape[1])
#             right_a, bottom_a = gray_max_h-grayA.shape[1],  gray_max_w-grayA.shape[0]
#             right_b, bottom_b = gray_max_h-grayB.shape[1],  gray_max_w-grayB.shape[0]
#             if (bottom_a, right_a) != (0, 0):
#                 grayA = cv2.copyMakeBorder(
#                     grayA, 0, bottom_a, 0, right_a,
#                     cv2.BORDER_CONSTANT, value=(0, 0, 0))
#             if (bottom_b, right_b) != (0, 0):
#                 o_grayB = grayB.copy()
#                 grayB = cv2.copyMakeBorder(
#                     grayB, 0, bottom_b, 0, right_b,
#                     cv2.BORDER_CONSTANT, value=(0, 0, 0))
#     else:

    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    print("SSIM Face: {}".format(score))
    return score

def check_workingtime():
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    detail_report = pd.DataFrame(columns = ['Time', 'Note', 'Image_Before', 'Image_After'])
    workingtime = 0
    freetime = 0
    timestep = 60
    # X1,Y1,X2,Y2
    X1 = 600
    Y1 = 300
    X2 = 1400
    Y2 = 700
    
    video_capture = cv2.VideoCapture(0)
    ret, frame_before2 = video_capture.read()
    screen_before2 = ImageGrab.grab(bbox=(X1,Y1,X2,Y2))
    # print(datetime.fromtimestamp(time.time()).strftime("%A, %B %d, %Y %I:%M:%S"))
    # plt.subplot(122), plt.imshow(frame_before2)
    # plt.subplot(121), plt.imshow(screen_before2)
    # plt.show()
    
    time.sleep(timestep)
    
    ret, frame_before1 = video_capture.read()
    screen_before1 = ImageGrab.grab(bbox=(X1,Y1,X2,Y2))
    # print(datetime.fromtimestamp(time.time()).strftime("%A, %B %d, %Y %I:%M:%S"))
    # plt.subplot(122), plt.imshow(frame_before1)
    # plt.subplot(121), plt.imshow(screen_before1)
    # plt.show()
    
    time.sleep(timestep)
    
    t_start = time.time()
    while True:
        # Stop
        if (time.time() - 3600) > t_start:
            video_capture.release()
            break
        t = time.time()    
        # Grabbing frames
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        screen = ImageGrab.grab(bbox=(X1,Y1,X2,Y2))
        video_capture.release()
        
        time_check = datetime.fromtimestamp(time.time()).strftime("%A, %B %d, %Y %I:%M:%S")
    #     print(time_check)
    #     plt.subplot(122), plt.imshow(frame)
    #     plt.subplot(121), plt.imshow(screen)
    #     plt.show()
            
        face_locations = face_recognition.face_locations(frame)
        
        if len(face_locations) == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
            if len(eyes) == 0:
                df_temp = pd.DataFrame(columns = ['Time', 'Note', 'Image_Before', 'Image_After'])
                df_temp['Time'] = [time_check]
                df_temp['Note'] = ['Can not detect face']      
                df_temp['Image_After'] = [frame]
                detail_report = pd.concat([detail_report, df_temp])
    
                freetime += timestep + time.time() - t
                
            else:
                workingtime += timestep + time.time() - t
                screen_before2 = screen_before1
                screen_before1 = screen
                frame_before2 = frame_before1
                frame_before1 = frame
        else:
                
            if (screen_diff(screen_before1, screen) > 0.8) and (screen_diff(screen_before2, screen) > 0.8):
                freetime += timestep + time.time() - t
                df_temp = pd.DataFrame(columns = ['Time', 'Note', 'Image_Before', 'Image_After'])
                df_temp['Time'] = [time_check]
                df_temp['Note'] = ['Screen no change']
                df_temp['Image_Before'] = [screen_before2]
                df_temp['Image_After'] = [screen]
                detail_report = pd.concat([detail_report, df_temp])
                
            elif (face_diff(frame_before1, frame) > 0.8) and (face_diff(frame_before2, frame) > 0.8):
                freetime += timestep + time.time() - t
                df_temp = pd.DataFrame(columns = ['Time', 'Note', 'Image_Before', 'Image_After'])
                df_temp['Time'] = [time_check]
                df_temp['Note'] = ['Webcam no change']
                df_temp['Image_Before'] = [frame_before2]
                df_temp['Image_After'] = [frame]
                detail_report = pd.concat([detail_report, df_temp])
        
            else:
                workingtime += timestep + time.time() - t
                screen_before2 = screen_before1
                screen_before1 = screen
                frame_before2 = frame_before1
                frame_before1 = frame
                
        print('working time: %ss - free time: %ss' % (workingtime, freetime))
        time.sleep(timestep)
     
#    video_capture.release()
    detail_report = detail_report.reset_index(drop=True)
    
    time_report = pd.DataFrame()
    time_report['Working Time'] = [workingtime]
    time_report['Free Time'] = [freetime]

    return time_report, detail_report
    
    
    
    
    
    
    