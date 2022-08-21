import cv2
import face_recognition as fr
import numpy as np


img= "C:\\Users\\Kaan\\Desktop\\20220805_195627.jpg"
kaan=cv2.imread(img)
rgb1=cv2.cvtColor(kaan,cv2.COLOR_BGR2RGB)
known_encoding= fr.face_encodings(rgb1)



cap = cv2.VideoCapture(0)
while True:
 _, frame = cap.read()
 rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
 bbox = fr.face_locations(rgb)
 encoding_compare=fr.face_encodings(rgb,bbox)
 for (h,w,y,x),cmp in zip(bbox,encoding_compare):

  comparisson=fr.compare_faces(known_encoding,cmp)
  #diff= fr.face_distance(known_encoding,cmp)     #BIRDEN FAZLA KISI TANIMAK ICIN KULLAN

  if comparisson[0]:
    cv2.putText(frame,"Kaan", (x + 10, y + 10), cv2.FONT_HERSHEY_DUPLEX ,1,(0,255,0),2)
    cv2.rectangle(frame, (x,y), (w,h), (0,255,0), 2)
  elif not comparisson[0]:
      cv2.putText(frame, "UNIDENTIFIED", (x + 10, y + 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
      cv2.rectangle(frame, (x, y), (w, h), (0, 0, 255), 2)




 cv2.imshow("rectangle",frame)




 if cv2.waitKey(31)== ord("q"):
     break
