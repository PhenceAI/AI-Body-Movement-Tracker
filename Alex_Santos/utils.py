#import dependencies
from datetime import datetime
import cv2
import mediapipe as mp
import math
import numpy as np
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
lmList = []
#some of our main fucntions for finding 
#postions and angles using MediaPipe

def findPose(img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            if draw:
                mpDraw.draw_landmarks(img, results.pose_landmarks,
                                           mpPose.POSE_CONNECTIONS)
        return img
    
def findPose2(img, draw=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        if draw:
            mpDraw.draw_landmarks(img, results.pose_landmarks,
                                        mpPose.POSE_CONNECTIONS)             
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            # print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    return img, lmList
    
"""
def findPosition(img, draw=True):
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            # print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    return lmList
"""
def findAngle(img, p1, p2, p3, draw=True):
    # Get the landmarks
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    x3, y3 = lmList[p3][1:]

    # Calculate the Angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                            math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360

    #print(angle)

    # Draw
    if draw:
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
        cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
        cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
        cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
        cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    return angle
