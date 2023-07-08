import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
#import mediapipe
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=HandDetector(detectionCon=1)
keys=[['Q','W','E','R','T','Y','U','I','O','P'],
     ['A','S','D','F','G','H','J','K','L',';'],
     ['Z','X','C','V','B','N','M',',','.','/']]
clickedtext=''
keyboard=Controller()
def draw_all(img,buttonlist):
    for button in buttonlist:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 60), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255), 2)
    return img
class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos = pos
        self.text = text
        self.size = size


# myButton = Button([100, 100],'Q')
buttonlist=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonlist.append(Button([100 * j + 100, 100 * i + 100], key))




while True:
    succcess,img=cap.read()
    img= cv2.flip(img, 1)
    detector.findHands(img)
    lmlist,bbox=detector.findPosition(img)
    draw_all(img, buttonlist)
    if lmlist:
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size

            if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 32, 56), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255), 3)
                l,_,_=detector.findDistance(8,12,img)
                if l<75:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (55, 32, 56), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255), 3)
                    clickedtext += button.text
                    sleep(2)
    cv2.rectangle(img, (100, 445),(1100,545), (0,0,0), cv2.FILLED)
    cv2.putText(img, clickedtext, (110,515), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255), 3)





    # draw_all(img, buttonlist)
    cv2.imshow('camera',img)
    cv2.waitKey(1)