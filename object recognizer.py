import cv2

cap=cv2.VideoCapture(0)
objects="D:\\PYTHON DENEMELERI\\OpenCV-object-detection-mobilenet-main\\coco.names"
list=[]
with open(objects) as file:
    list=file.read().strip("\n").split("\n")
    print(list)

config="D:\\PYTHON DENEMELERI\\OpenCV-object-detection-mobilenet-main\\frozen_inference_graph.pb"
weights="D:\\PYTHON DENEMELERI\\OpenCV-object-detection-mobilenet-main\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

model=cv2.dnn_DetectionModel(weights,config)

model.setInputSize(320,320)
model.setInputMean(127.5)
model.setInputScale(1.0/127.5)
model.setInputSwapRB(True)
#model.setInputCrop(False)

while True:
   _,frame=cap.read()

   classIDS,confidences,boxes=model.detect(frame,confThreshold=0.5)

   for cl,cn,bbox in zip(classIDS,confidences,boxes):
       cv2.rectangle(frame,bbox,(255,0,0),2)
       cv2.putText(frame,list[cl-1],(bbox[0]+10,bbox[1]+10),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,0),2)


   cv2.imshow("object recognizer",frame)
   if cv2.waitKey(31)==ord("q"):
       break