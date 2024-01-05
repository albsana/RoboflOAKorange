#####################################################################################TIEMPO REAL#########################################################################################


import naranja
import os
import pandas as pd
import wx
import threading
import cv2
#import recording
from ultralytics import YOLO
import depthai as dai

from tracker import*
from glob import glob
from torchvision.utils import draw_bounding_boxes
#from IPython.display import Image, display


####################################
# Class NaranjasFrame
####################################

class naranjasFrameImpl (naranja.naranjaFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.detectButton.Bind(wx.EVT_BUTTON, self.iniciarProcesoDetectar)
        #self.stopButton.Bind(wx.EVT_BUTTON, self.iniciarProcesoStop)
        self.closeButton.Enable()
        #self.grabacionButton.Bind(wx.EVT_BUTTON, self.grabacionProceso)
        self.tracker=Tracker()
        self.detenerButton
        self.stopVideoFlag = False        
############Variables###############

        self.count=0
        self.cy1=200
        self.cy2=525
        self.cy3=850
        self.offset=10
        self.oran_pass={}
        self.counter1 = set()
        self.counter2 = set()
        self.counter3 = set()
        self.estimacion = 0
        self.long1 = 0
        self.long2 = 0
        self.long3 = 0

###########Create pipeline############
        
    def pipeline(self):

        pipeline = dai.Pipeline()

        # Define source and output
        camRgb = pipeline.create(dai.node.ColorCamera)
        xoutVideo = pipeline.create(dai.node.XLinkOut)

        xoutVideo.setStreamName("video")

        # Properties
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
        camRgb.setVideoSize(1080, 720)

        camRgb.setInterleaved(False)
        #If following downscale process is uncommented, frame drops doesn't happen
        camRgb.setIspScale(2, 3)
        xoutVideo.input.setBlocking(False)
        xoutVideo.input.setQueueSize(1)

        # Linking
        camRgb.video.link(xoutVideo.input)

        
        # camRgb = pipeline.create(dai.node.ColorCamera)
        # camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        # camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

        # xoutRgb = pipeline.create(dai.node.XLinkOut)
        # xoutRgb.setStreamName("rgb")
        # camRgb.video.link(xoutRgb.input)

        # xin = pipeline.create(dai.node.XLinkIn)
        # xin.setStreamName("control")
        # xin.out.link(camRgb.inputControl)

        # # Properties
        # videoEnc = pipeline.create(dai.node.VideoEncoder)
        # videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
        # camRgb.still.link(videoEnc.input)

        # # Linking
        # xoutStill = pipeline.create(dai.node.XLinkOut)
        # xoutStill.setStreamName("still")
        # videoEnc.bitstream.link(xoutStill.input)
        
        
        
        return pipeline


#############Recording##############

    def grabacionProceso(self, event):
        self.grabacionButton.Disable()
        self.quitRecording = threading.Event()
        self.thread = threading.Thread(target= self.recording, args=[self.quitRecording])
        self.thread.start()

    def recording(self, threadEvent):
        recording.run(threadEvent)
        
    def stopRecording(self):
        self.quitRecording.set()
        self.grabacionButton.Enable()

####################################

    def iniciarProcesoDetectar(self, event):
        self.detectButton.Disable()
        self.thread = threading.Thread(target=self.detectarRecortar)
        self.thread.start()

    # def iniciarProcesoStop(self, event):
    #     self.stopButton.Disable()
    #     self.thread = threading.Thread(target=self.stopButtonFunc)
    #     self.thread.start()

    def stopVideo(self):
        
        if self.stopVideoFlag == True:
            self.closeButton.Enable()
            return self.stopVideoFlag

    def cargaModelo(self):
        
        model=YOLO(r'F:\Alberto\Interfaz\yolov8n_custom20\weights\best.pt')
        return model
    
    def detectar(self):
        self.closeButton.Disable()
        self.counter1.clear()
        self.counter2.clear()
        self.counter3.clear()
        self.medidasText.Clear()
        self.estimaciontextCtrl.Clear()
        self.medidasText.AppendText("Conteo iniciado...   ")
        modelo = self.cargaModelo()
        pipeline = self.pipeline()

        count = self.count
        cy1 = self.cy1
        cy2 = self.cy2
        cy3 = self.cy3
        offset = self.offset
        oran_pass = self.oran_pass
        counter1 = self.counter1
        counter2 = self.counter2
        counter3 = self.counter3
        estimacion = self.estimacion
        long1 = self.long1
        long2 = self.long2
        long3 = self.long3

        with dai.Device(pipeline) as device:

            video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

            while True:    
                
                videoIn = video.get()
            
                frame = videoIn.getCvFrame()
        # with dai.Device(pipeline) as device:

        #     # Output queue will be used to get the rgb frames from the output defined above
        #     qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)

        #     while True:
        #         inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
        #         if inRgb is not None:
        #             frame = inRgb.getCvFrame()
        #             # 4k / 4
        #             #frame = cv2.pyrDown(frame)
        #             frame = cv2.pyrDown(frame)
        #             #cv2.imshow("rgb", frame)

                class_list = modelo.names
                results=modelo.predict(frame)
                results[0].conf = 0.35

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

                bbox_id=self.tracker.update(list)
                for bbox in bbox_id:
                    x3,y3,x4,y4,id=bbox
                    cx=int(x3+x4)//2
                    cy=int(y3+y4)//2
                    cv2.rectangle(frame, (x3,y3), (x4,y4), (0, 0, 255), 2)

                    if cy1<(cx+offset) and cy1> (cx-offset):
                        oran_pass[id] = cx
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                        counter1.add(id)
                        long1 = len(counter1)

                    if cy2<(cx+offset) and cy2> (cx-offset):
                        oran_pass[id] = cx
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                        counter2.add(id)
                        long2 = len(counter2)

                    if cy3<(cx+offset) and cy3> (cx-offset):
                        oran_pass[id] = cx
                        cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                        cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)       
                        counter3.add(id)
                        
                        long3 = len(counter3)

                cv2.line(frame,(cy1, 725), (cy1, 10),(255,255,255),1)
                cv2.line(frame,(cy2, 725), (cy2, 10),(255,255,255),1)
                cv2.line(frame,(cy3, 725), (cy3, 10),(255,255,255),1)

                estimacion = (long1 + long2 + long3)/3
                estimacion = int(estimacion)
                try:
                    self.estimaciontextCtrl.SetValue(f'Linea1:  {long1}\nLinea2:  {long2}\nLinea3:  {long3}\n' + 'Estimación: ' + str(estimacion))    
                except RuntimeError:
                    self.Close()
                    
                cv2.putText(frame, ('Naranjas: ') + str(estimacion), (cy1, 50), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
                cv2.imshow("RGB", frame)
                if cv2.waitKey(1)&0xFF==27:
                    break
        
                if cv2.waitKey(1) == ord('q'):
                    break  
                if self.stopVideo() == True:
                    break
    
        cv2.destroyAllWindows()
        os.makedirs("F:/Alberto/Interfaz/Datos/", exist_ok=True)
        path = 'F:/Alberto/Interfaz/Datos/Estimacion.xlsx'
        df = pd.DataFrame({'Estimacion 1' : [long1],
                           'Estimacion 2' : [long2],
                           'Estimacion 3' : [long3],
                           'Estimacion Final' : [estimacion],})
        
        if os.path.exists(path):
            df_existe = pd.read_excel(path)
            df = pd.concat([df_existe, df], ignore_index=True)
        
        df.to_excel(path,index=False)

        wx.CallAfter(self.detectButton.Enable)
        self.medidasText.AppendText("Finalizado.")
        self.stopVideoFlag = False
    


###################################
# Botones Main
###################################

    def detectarRecortar(self):
        self.detectar()

    def stopButtonFunc(self, event):
        self.stopVideoFlag = True
        self.stopVideo()

    def grabacionFunction(self, event):
        self.recording()     
    
    def grabacionStopFunction(self, event):
        self.stopRecording()

    def closeFunc(self, event):
        self.Close()

###################################
