import cv2
import mediapipe as mp
import numpy as np
import math
from pynput.mouse import Button,Controller

mouse=Controller()

width_cam=640
height_cam=480
width_screen=1920
height_screen=1080

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH ,width_cam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height_cam)

origin=mp.solutions.hands
hand=origin.Hands()
landmarks=mp.solutions.drawing_utils
color=(0,255,0)




while True:
    _,frame=cap.read()
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    process=hand.process(rgb)
    avaliable=process.multi_hand_landmarks  #process MODULUNDE return'LER COMMENT OLARAK BELIRTILIS multi_hand_landmarks DA ONLARDAN BIRI

    if avaliable :    #ANLAMADIM

        for lndmrks in avaliable:

         list=[]                           #!!!!!!!!!!EGER list'i burada declare etmezsem sadece ilk frame'in verilerini store'luyor ama benim, degerlerin surekli degismesine ihtiyacim var

         for id,ln in enumerate(lndmrks.landmark):     #HICBIR FIKRIM YOK \ enumerate'yi ogren
          #print(frame.shape)
          x,y,z=frame.shape                             #PENCERENIN PIXEL BOYUTUNU ANLAMAK ICIN KULLANILAN cv2 FONKSIYONU SIRASIYLA X, Y VE Z AXISLERINI VERIYOR
          x1=int(ln.x*y)                                # LANDMARK(ln) POZISYONLARI PENCERENIN BOYUTUNA ORANLI OLDUGU ICIN DEGERLERI GUNCELLEYIP VERDIK
          y1=int(ln.y*x)
          #print(x1,y1)
          list.append([id,x1,y1])                           #ASIRI ONEMLI!!!!!! =>>  id, x1 ve y1 degerleri intiger idi ve bunlari bir liste icine koymam gerekiyprdu bu yontemle yaptim

    if avaliable:

     for lndmrks in avaliable:

      for id,ln in enumerate(lndmrks.landmark):

       if len(list) != 0:                           #ERROR'U GIDERMEK ICIN INSANLAR HEP BU YONTEMI KULLANIYOR ISE DEYARIYOR VALLAHI


              fx ,fy= list[8][1], list[8][2]

              ex,ey = list[12][1], list[12][2]

              hypo = math.hypot((ex - fx), (ey - fy))

              x3 = np.interp(fx,(0,width_cam),(0,width_screen))
              y3=np.interp(fy,(0,height_cam),(0,height_screen))

              if fy<list[6][2] and ey>list[10][2]:
                  print("    M O V I N G")
                  cv2.circle(frame,(fx,fy),20,(255,0,0),cv2.FILLED)
                  mouse.position=(x3,y3)

              elif fy<list[6][2] and ey<list[10][2]:
                 if hypo<20:
                   print("CLICKING")
                   mouse.click(Button.left,1)

       landmarks.draw_landmarks(frame, lndmrks,mp.solutions.hands_connections.HAND_CONNECTIONS)  # goruntu kismina BGR GORUNTU KONULUYOR!!!!\
                                                                                                # draw_landmarks MODULU 3. arg OLARAK connections istiyor bunun icin de\
                                                                                          # GEREKLI "HAND_CONNECTIONS" methoduna ULASIYORUZ!!!!

    #cv2.rectangle(frame, (cx-w//2,cy-h//2),(cx+w//2,cy+h//2), color, cv2.FILLED)
    cv2.imshow("hand",frame)
    if cv2.waitKey(1)==ord("q"):
        break