import  cv2

cap= cv2.VideoCapture(0)
first_image=None

while True:
  _,frame=cap.read()
  gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
  gaussian_blur=cv2.GaussianBlur(gray,(9,9),2)
  blur=cv2.blur(gaussian_blur,(3,3))
  if first_image is None:
      first_image=blur
  else :
      pass

  #diff=cv2.absdiff(first_image,blur)
  thresh = cv2.threshold(blur, 90,255, cv2.THRESH_BINARY)[1]
  dilation=cv2.dilate(thresh,(3,3))
  contour=cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]
  for c in contour:
     area=cv2.contourArea(c)
     if area >500 and area<3000:

         (x,y,w,h)=cv2.boundingRect(c)

         cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

  cv2.imshow("dilation",dilation)
  cv2.imshow("sensor",frame)
  if cv2.waitKey(31) == ord("q"):
   break