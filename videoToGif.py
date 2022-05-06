import cv2
import os
import math
import numpy as np
import imageio
from PIL import Image
from cvzone.PoseModule import PoseDetector
video_name = 'video.mp4'
SIZE_SMALL = 256

image_lst = []

def maxRadius(img, lmList, centerX, centerY):
    maxR = 0
    for lmItem in lmList:        
        index, x, y = lmItem[:]
        maxR = max(maxR, math.hypot(x - centerX, y - centerY))
    return maxR

def normaliseList(img, lmList, centerX, centerY): 
    for i in range (0, 29):              
        lmList[i][1] = lmList[i][1] +  centerX
        lmList[i][2] = lmList[i][2] +  centerY            
        
def normaliseRatio(img, lmList):   
    x1 = ( lmList[11][1] + lmList[12][1] ) // 2
    y1 = ( lmList[11][2] + lmList[12][2] ) // 2        
    x2 = ( lmList[23][1] + lmList[24][1] ) // 2
    y2 = ( lmList[23][2] + lmList[24][2] ) // 2        
    
    length = math.hypot(x2 - x1, y2 - y1)+0.1
    diameter = 2.0*1.6*length
    ratio = SIZE_SMALL/diameter    
    for i in range (0, 29):        
        lmList[i][1] = int(lmList[i][1] * ratio)
        lmList[i][2] = int(lmList[i][2] * ratio)
        
def drawLine(img, lmList, one, two):
    x1, y1 = lmList[one][1:]
    x2, y2 = lmList[two][1:]
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
    
def drawBodyLines(img, lmList):
    if len(lmList) > 0:    
        drawLine(img, lmList, 11, 12)
        drawLine(img, lmList, 12, 14)
        drawLine(img, lmList, 14, 16)
        drawLine(img, lmList, 11, 13)
        drawLine(img, lmList, 13, 15)
        drawLine(img, lmList, 23, 24)
        
        drawLine(img, lmList, 23, 25)
        drawLine(img, lmList, 25, 27)
        
        drawLine(img, lmList, 24, 26)
        drawLine(img, lmList, 26, 28)       
        

def drawCenterAndRadius(img, lmList):
    x0 = lmList[0][1]
    y0 = lmList[0][2]    
    x1 = ( lmList[11][1] + lmList[12][1] ) // 2
    y1 = ( lmList[11][2] + lmList[12][2] ) // 2        
    x2 = ( lmList[23][1] + lmList[24][1] ) // 2
    y2 = ( lmList[23][2] + lmList[24][2] ) // 2        
    cv2.line(img, (x1, y1), (x0, y0), (255, 255, 255), 2)
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)    
    length = math.hypot(x2 - x1, y2 - y1)
    return length

detector = PoseDetector()

counter = 0
cap = cv2.VideoCapture(video_name)

#for image in images:
while(cap.isOpened()):
    ret, imageCV = cap.read()  
    if not ret:
        break
    #print (ret)
    counter = counter + 1
    if counter % 15 != 0:
        continue
        
    height, width, layers = imageCV.shape    
    #imageOrig = cv2.resize(imageCV, (6*SIZE_SMALL, 4*SIZE_SMALL))   
    
    img = detector.findPose(imageCV, draw=False)
    img[:]=[0, 0, 0]
    lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)
    length = 0
    
    if len(lmList) > 0: 
        normaliseRatio(img, lmList)
        x2 = ( lmList[23][1] + lmList[24][1] ) // 2
        y2 = ( lmList[23][2] + lmList[24][2] ) // 2    
        normaliseList(img, lmList, width//2 - x2, height//2 - y2)
        drawBodyLines(img, lmList)
        length = drawCenterAndRadius(img, lmList)
    
    smallimg = img[height//2-int(1.6*length):height//2+int(1.6*length), width//2-int(1.6*length):width//2+int(1.6*length)]
    smallimg = 255-cv2.resize(smallimg, (SIZE_SMALL, SIZE_SMALL), interpolation = cv2.INTER_AREA)
    cv2.imshow("small", smallimg)  
    image_lst.append(smallimg)
    
    k = cv2.waitKey(1)
    if k==27:    # Esc key to stop        
        break
    
    
    
# Convert to gif using the imageio.mimsave method
imageio.mimsave('video.gif', image_lst, fps=2)    
#image_lst[0].save('video.gif', save_all=True, append_images=image_lst[1:])
cv2.destroyAllWindows()
#video.release()