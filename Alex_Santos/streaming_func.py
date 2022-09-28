import cv2
import Alex_Santos.PoseModule as pm
from datetime import datetime
import os
import csv
import time



detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0


# function for getting frame from external source and
# processing it and saving the data to a csv file
def process_frame(frame):
    global detector
    global count
    global dir
    global pTime
    # writing csv headers and initilizing csv
    #headers for our CSV file
    header = ['Timestamp', 'Right_Arm_Angle', 'Left_Arm_Angle', 'Right_Leg_Angle',  'Left_Leg_Angle',
                'Nose', 'Left Inner Eye', 'Left Eye', 'Left Outter Eye', 'Right Inner Eye', 
                'Right Eye', 'Right Outter Eye', 'Left Ear', 'Right Ear', 'Mouth Left', 'Mouth Right',
                'Left Shoulder', 'Right Shoulder', 'Left Elbow', 'Right Elbow', 'Left Wrist', 
                'Right Wrist', 'Left Pinky', 'Right Pinky', 'Left Index', 'Right Index', 
                'L-Thmb', 'R-Thmb', 'L Hip', 'sR Hip', 'L-Knee', 'R-Knee', 'L-Ankle', 'R-Ankle', 
                'L-Heel', 'R-Heel', 'L-Foot-Index', 'R-Foot-Index']
    filename = open("Alex_Santos/fl.txt", "r").read()
    file_existance = os.path.exists(filename)
    csv_file = open(filename, mode="a+", encoding="utf-8", newline="")
    writer = csv.DictWriter(csv_file, fieldnames=header)

    img = frame
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, True)
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
    return cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)



