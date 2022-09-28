from asyncore import write
import cv2
import numpy as np
import time
import Alex_Santos.PoseModule as pm
import argparse
from datetime import datetime
import imutils
import os
import csv
import time

#construct argurment parser and parse args
ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', type = str, required = True, default = None,
                help = 'path to input image or video')
args = vars(ap.parse_args())

#headers for our CSV file
header = ['Timestamp', 'Right_Arm_Angle', 'Left_Arm_Angle', 'Right_Leg_Angle',  'Left_Leg_Angle',
            'Nose', 'Left Inner Eye', 'Left Eye', 'Left Outter Eye', 'Right Inner Eye', 
            'Right Eye', 'Right Outter Eye', 'Left Ear', 'Right Ear', 'Mouth Left', 'Mouth Right',
            'Left Shoulder', 'Right Shoulder', 'Left Elbow', 'Right Elbow', 'Left Wrist', 
            'Right Wrist', 'Left Pinky', 'Right Pinky', 'Left Index', 'Right Index', 
            'L-Thmb', 'R-Thmb', 'L Hip', 'sR Hip', 'L-Knee', 'R-Knee', 'L-Ankle', 'R-Ankle', 
            'L-Heel', 'R-Heel', 'L-Foot-Index', 'R-Foot-Index']

# writing csv headers and initilizing csv
filename = "video_data.csv"
file_existance = os.path.exists(filename)
csv_file = open(filename, mode="a+", encoding="utf-8", newline="")
writer = csv.DictWriter(csv_file, fieldnames=header)

if not file_existance:
    writer.writeheader()
    

cap = cv2.VideoCapture(args["video"])

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    
    # coordinates, angles and timestamp
    if len(lmList) != 0:
        # Right Arm
        right_arm_angle = detector.findAngle(img, 12, 14, 16)
        
        # # Left Arm
        left_arm_angle = detector.findAngle(img, 11, 13, 15)
        
        #right leg
        right_leg_angle = detector.findAngle(img, 24, 26, 28,True)
        
        #left leg
        left_leg_angle = detector.findAngle(img, 23, 25, 27,True)
        
        # per = np.interp(angle, (210, 310), (0, 100))
        # bar = np.interp(angle, (220, 310), (650, 100))
        # print(angle, per)

        # Check for the dumbbell curls
        # color = (255, 0, 255)
        # if per == 100:
        #     color = (0, 255, 0)
        #     if dir == 0:
        #         count += 0.5
        #         dir = 1
        # if per == 0:
        #     color = (0, 255, 0)
        #     if dir == 1:
        #         count += 0.5
        #         dir = 0
        #print(count)

        """
        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    #(255, 0, 0), 25)
        """

    # ************csv writing part**************
    data = {
        'Timestamp': datetime.now(),
        'Right_Arm_Angle': right_arm_angle,
        'Left_Arm_Angle' : left_arm_angle,
        'Right_Leg_Angle' : right_leg_angle,
        'Left_Leg_Angle' : left_leg_angle,
        'Nose': lmList[0],
        'Left Inner Eye' : lmList[1],
        'Left Eye'  : lmList[2],
        'Left Outter Eye'  : lmList[3],
        'Right Inner Eye' : lmList[4],
        'Right Eye'  : lmList[5],
        'Right Outter Eye' : lmList[6],
        'Left Ear'  : lmList[7],
        'Right Ear'  : lmList[8],
        'Mouth Left' : lmList[9],
        'Mouth Right'  : lmList[10],
        'Left Shoulder' : lmList[11],
        'Right Shoulder' : lmList[12],
        'Left Elbow' : lmList[13],
        'Right Elbow'  : lmList[14],
        'Left Wrist'  : lmList[15],
        'Right Wrist'  : lmList[16],
        'Left Pinky'   : lmList[17],
        'Right Pinky'  : lmList[18],
        'Left Index' : lmList[19],
        'Right Index' : lmList[20],
        'L-Thmb'  : lmList[21],
        'R-Thmb'   : lmList[22],
        'L Hip'  : lmList[23],
        'sR Hip'  : lmList[24],
        'L-Knee'  : lmList[25],
        'R-Knee' : lmList[26],
        'L-Ankle' : lmList[27],
        'R-Ankle'  : lmList[28],
        'L-Heel'  : lmList[29],
        'R-Heel'  : lmList[30],
        'L-Foot-Index'  : lmList[31],
        'R-Foot-Index'  : lmList[32],
    }
    
    writer.writerow(data)
    # ************csv writing end part*****************
    
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)


