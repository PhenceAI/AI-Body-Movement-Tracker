import cv2
import time
import mediapipe as mp
from utils import findAngle, findPose, findPose2
import argparse
import imutils
import csv
from datetime import datetime

#construct argurment parser and parse args
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', type = str, required = True, default = None,
                help = 'path to input image')
args = vars(ap.parse_args())

##Set up Mediapipe ##
#initialize the drawing capabilities of mp
#initialize the pose model from mp
#instantiate the pose model
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

#optional variables used for exercise counts
count = 0
dir = 0
pTime = 0

#Images ##
img = cv2.imread(args['image'])
img = imutils.resize(img, width= 720)
    
#find poses, positions and angles
#img = findPose(img, True)
imgList = findPose2(img)
#lmList = findPosition(img, True)
# print(imgList)
    
if len(imgList) != 0:
    # Right Arm
    rarm = findAngle(img, 12, 14, 16, False)
    # print(rarm)
        
    # Left Arm
    larm = findAngle(img, 11, 13, 15, False)
    # print(larm)
        
    #right leg
    rleg = findAngle(img, 24, 26, 28,True)
    # print(rleg)
        
    #left leg
    lleg = findAngle(img, 23, 25, 27,True)
    # print(lleg)

cTime = time.time()
fps = 1 / (cTime - pTime)
pTime = cTime
cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
            (255, 0, 0), 5)

cv2.imshow("Image", img)
cv2.waitKey(0)



 
    
# writing data row-wise into the csv file


# writing the data into the file
with open(r'pose2.csv', 'a+', newline ='') as csvfile:
    header = ['Timestamp', 'Img', 'lmList']
    writer = csv.DictWriter(csvfile, fieldnames = header)
    writer.writeheader()
    current_date_time = datetime.now()
    data = {
        'Timestamp': current_date_time,
        'Img': [i for i in img[0]],
        'lmList': [i for i in img[1]], 
    }
    writer.writerow(data)

#with open('./file.txt', 'wb') as file:
#        pickle.dump(imgList, file)