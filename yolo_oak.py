import cv2
import depthai as dai
from ultralytics import YOLO
import pandas as pd
from tracker import*
tracker=Tracker()

modelo = YOLO(r"C:\Users\Usuario\runs\detect\Yolov8n\weights\best.pt")
# Create pipeline
pipeline = dai.Pipeline()


# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
#camRgb.setVideoSize(1080, 720)

camRgb.setInterleaved(False)
#If following downscale process is uncommented, frame drops doesn't happen
camRgb.setIspScale(2, 3)
xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

# Linking
camRgb.video.link(xoutVideo.input)

with dai.Device(pipeline) as device:
    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)
    while True:

                videoIn = video.get()

                frame = videoIn.getCvFrame()
                class_list = modelo.names

                results=modelo.predict(frame)

                a=results[0].boxes.data.cpu()
                px=pd.DataFrame(a).astype("float")
                list=[]
                

                

                for index,row in px.iterrows():

                        x1=int(row[0])
                        y1=int(row[1])
                        x2=int(row[2])
                        y2=int(row[3])
                        d=int(row[5])
                        c=class_list[d]

                        if 'Naranja' in c:
                            list.append([x1,y1,x2,y2])
                                
                
                bbox_id=tracker.update(list)

                for bbox in bbox_id:
                        x3,y3,x4,y4,id=bbox
                        cx=int(x3+x4)//2
                        cy=int(y3+y4)//2
                        cv2.rectangle(frame, (x3,y3), (x4,y4), (0, 0, 255), 2)

                cv2.imshow("RGB", frame)


                if cv2.waitKey(1) == ord('q'):
                       break

