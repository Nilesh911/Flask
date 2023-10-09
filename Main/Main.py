from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np

app = Flask(__name__)

@app.route('/')

def index():
    return render_template ('index.html')

def move_forward():
  
cap = cv2.VideoCapture(0)

detector = PoseDetector(detectionCon=0.69)
color = (0,0,255)
dir = 0
curl_count = 0
# 38-140
while True:

    _, img = cap.read()
    img = detector.findPose(img)
    lmlist,bbox = detector.findPosition(img,draw = False)
    if lmlist:
        # print(lmlist)

        angle = detector.findAngle(img,12,14,16)


        bar_val = np.interp(angle(38,140),(60,300+60))

        per_val = np.interp(angle,(38,140),(100,0))


        cv2.rectangle(img,(560,int(bar_val)),(40+560,300+60),color,cv2.FILLED)

        cv2.rectangle(img,(590,60),(40+590,300+60),(0,0,0),9)
        # (x,y),(x+w),(y+h)
        cvzone.putTextRect(img,f"{int(per_val)} %",(540,40),1.6,2,(255,255,255),color,border=4,colorB=())
        # print(angle)

        if per_val == 100:
            if dir == 0:
                curl_count += 0.5
                dir = 1
                color = (0, 255, 0)
        elif per_val == 0:
            if dir == 1:
                curl_count += 0.5
                dir = 0
                color = (0,255,0)
        else:
            color = (0,0,255)
        print(curl_count)


    cvzone.putTextRect(img,'BICEP CURL COUNTER!!',(50,40),2,3,(255,255,255),(255,0,0),border=6,colorB=())


    cvzone.putTextRect(img, f'Curl Count : {int(curl_count)}', (30, 120), 2, 3, (255, 255, 255), (0, 155, 0), border=6, colorB=())


    cv2.imshow('Bicep counter', img)

    if cv2.waitKey(1) == ord('Esc'):
        break


    print("Moving forward")

if __name__=='__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)