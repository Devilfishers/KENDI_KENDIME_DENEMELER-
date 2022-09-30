import cv2
import numpy as np
import RPi.GPIO as rg
import  pygame
import math

pygame.init()
pygame.display.set_mode(size=(100,100))

cap = cv2.VideoCapture("/dev/video0")

rg.setmode(rg.BCM)

rg.setup(18, rg.OUT)
rg.setup(22,rg.OUT)
ENA=rg.PWM(18,100)
ENB=rg.PWM(22,100)
rg.setup(23,rg.OUT)
rg.setup(24,rg.OUT)
rg.setup(17,rg.OUT)
rg.setup(27,rg.OUT)

ENB.start(0)
ENA.start(0)

rg.setwarnings(False)

I= int()
K= int()
D= int()

Kp= 0.05
Ki= 0.0009
Kd= 2

baseA=10
baseB=10

maxA=50
maxB=50

lastError=0

def forward(pwmA,pwmB):
 rg.output(23 ,rg.LOW)
 rg.output(24, rg.HIGH)
 rg.output(27, rg.HIGH)
 rg.output(17, rg.LOW)
 ENA.ChangeDutyCycle(pwmA)
 ENB.ChangeDutyCycle(pwmB)



def PID_control(offset):

 global P
 global I
 global D
 global lastError

 error = 345- offset
 P= error
 I= I + error
 D= error - lastError
 lastError=error


 movement= (Kp*P) + (Ki*I) + (Kd*D)
 #movement=float(movement)
 speedA= baseA + movement
 speedB= baseB - movement

 if speedA > maxA:
     speedA = maxA
 if speedB > maxB:
     speedB = maxB
 if speedA < 0:
     speedA = 0
 if speedB < 0:
     speedB = 0
 forward(speedA,speedB)

while True:
    for event in pygame.event.get():
        pass
    ret, frame = cap.read()
    low_b = np.uint8([21,21,21])
    high_b = np.uint8([0,0,0])
    mask = cv2.inRange(frame, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
         cx = int(M['m10'] / M['m00'])
         cy = int(M['m01'] / M['m00'])
         print("CX : " + str(cx) + "  CY : " + str(cy))

         PID_control(cx)



    cv2.imshow("Mask",mask)


    if cv2.waitKey(1) == ord('q'):
        rg.cleanup()
        break
cap.release()
cv2.destroyAllWindows()
