import cv2
import math
import depthai as dai
from datetime import timedelta
import numpy as np
from ultralytics import YOLO
import pandas as pd
from tracker import*
tracker=Tracker()

class HostSpatialsCalc:
    # We need device object to get calibration data
    def __init__(self, device):
        self.calibData = device.readCalibration()

        # Values
        self.DELTA = 5
        self.THRESH_LOW = 50 # 20cm
        self.THRESH_HIGH = 2000 # 30m

    def setLowerThreshold(self, threshold_low):
        self.THRESH_LOW = threshold_low
    def setUpperThreshold(self, threshold_low):
        self.THRESH_HIGH = threshold_low
    def setDeltaRoi(self, delta):
        self.DELTA = delta

    def _check_input(self, roi, frame): # Check if input is ROI or point. If point, convert to ROI
        if len(roi) == 4: return roi
        if len(roi) != 2: raise ValueError("You have to pass either ROI (4 values) or point (2 values)!")
        # Limit the point so ROI won't be outside the frame
        self.DELTA = 5 # Take 10x10 depth pixels around point for depth averaging
        x = min(max(roi[0], self.DELTA), frame.shape[1] - self.DELTA)
        y = min(max(roi[1], self.DELTA), frame.shape[0] - self.DELTA)
        return (x-self.DELTA,y-self.DELTA,x+self.DELTA,y+self.DELTA)

    def _calc_angle(self, frame, offset, HFOV):
        return math.atan(math.tan(HFOV / 2.0) * offset / (frame.shape[1] / 2.0))

    # roi has to be list of ints
    def calc_spatials(self, depthData, roi, averaging_method=np.mean):

        depthFrame = depthData.getFrame()

        roi = self._check_input(roi, depthFrame) # If point was passed, convert it to ROI
        xmin, ymin, xmax, ymax = roi

        # Calculate the average depth in the ROI.
        depthROI = depthFrame[ymin:ymax, xmin:xmax]
        inRange = (self.THRESH_LOW <= depthROI) & (depthROI <= self.THRESH_HIGH)

        # Required information for calculating spatial coordinates on the host
        HFOV = np.deg2rad(self.calibData.getFov(dai.CameraBoardSocket(depthData.getInstanceNum())))

        averageDepth = averaging_method(depthROI[inRange])

        centroid = { # Get centroid of the ROI
            'x': int((xmax + xmin) / 2),
            'y': int((ymax + ymin) / 2)
        }

        midW = int(depthFrame.shape[1] / 2) # middle of the depth img width
        midH = int(depthFrame.shape[0] / 2) # middle of the depth img height
        bb_x_pos = centroid['x'] - midW
        bb_y_pos = centroid['y'] - midH

        angle_x = self._calc_angle(depthFrame, bb_x_pos, HFOV)
        angle_y = self._calc_angle(depthFrame, bb_y_pos, HFOV)

        spatials = {
            'z': averageDepth,
            'x': averageDepth * math.tan(angle_x),
            'y': -averageDepth * math.tan(angle_y)
        }
        return spatials, centroid

model = YOLO(r"D:\TDG_Alejo\Codigos\runs\detect\yolov8x\weights\best.engine")

## Crear las tuberias
pipeline = dai.Pipeline()

## Definir tuberias de  entradas y salidas  
RgB = pipeline.create(dai.node.ColorCamera)
Left = pipeline.create(dai.node.MonoCamera)
Right = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth) ## El nodo StereoDepth calcula la disparidad y/o profundidad del par de cámaras estéreo (2x MonoCamera / ColorCamera ).
#sync = pipeline.create(dai.node.Sync) ## El nodo Sync se utiliza para sincronizar múltiples flujos de entrada en función de sus marcas de tiempo.

### El nodo XLinkOut se utiliza para enviar datos desde el dispositivo al host a través de XLink.
xoutRgB = pipeline.create(dai.node.XLinkOut)
xoutDepth = pipeline.create(dai.node.XLinkOut)

### SetStreamName Especifica el nombre de la secuencia XLink que se utilizará.
xoutRgB.setStreamName("rgb")
xoutDepth.setStreamName("depth")

## Definir las propiedades de cada flujo o secuencia
RgB.setPreviewSize(416, 416)
RgB.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
RgB.setInterleaved(False)
RgB.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

Left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
Left.setCamera("left")
Right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
Right.setCamera("right")

stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_ACCURACY)
stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)
stereo.setOutputSize(Left.getResolutionWidth(), Left.getResolutionHeight())
stereo.setSubpixel(True)

#sync.setSyncThreshold(timedelta(milliseconds=50))

## Realizar las conexiones
### PREVIEW Genera un mensaje ImgFrame que transporta datos de cuadros codificados planos/intercalados BGR/RGB.
### LINK Vincular la salida a una entrada. Ambos nodos deben estar en la misma tubería.
### OUTPUT Salida de nodos desde los que conectarse
### INPUT Entrada de nodos para conectarse

RgB.preview.link(xoutRgB.input)
Left.out.link(stereo.left)
Right.out.link(stereo.right)
stereo.depth.link(xoutDepth.input)


disparityMultiplier = 255.0 / stereo.initialConfig.getMaxDisparity()

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
        
        spatial_calculator = HostSpatialsCalc(device)
        
        ### getOutputQueue, para recibir mensajes en el host desde el dispositivo (puede enviar el mensaje en el dispositivo con XLinkOut)
        qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        qDepth = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
       
        while True:

                RgbIn = qRgb.get()
                DepthIn = qDepth.get()

                frame = RgbIn.getCvFrame()
                depthframe = DepthIn.getFrame()

                depth_downscaled = depthframe[::4]
                if np.all(depth_downscaled == 0):
                    min_depth = 0  # Set a default minimum depth value when all elements are zero
                else:
                    min_depth = np.percentile(depth_downscaled[depth_downscaled != 0], 1)
                max_depth = np.percentile(depth_downscaled, 99)
                depthFrameColor = np.interp(depthframe, (min_depth, max_depth), (0, 255)).astype(np.uint8)
                depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)

                
                class_list = model.names
                results=model.predict(frame)
                results[0].conf = 0.20


                a=results[0].boxes.data.cpu()
                px=pd.DataFrame(a).astype("float")
                detecciones=[]
                

                for index,row in px.iterrows():

                        x1=int(row[0])
                        y1=int(row[1])
                        x2=int(row[2])
                        y2=int(row[3])
                        d=int(row[5])
                        c=class_list[d]

                        if 'Naranja' in c:
                            detecciones.append([x1,y1,x2,y2])
                                
                
                bbox_id=tracker.update(detecciones)

                for bbox in bbox_id:
                        x3,y3,x4,y4,id=bbox

                        print(depthframe)
 

                        # Calcular las coordenadas espaciales
                        roi = [x3, y3, x4, y4]
                        spatials, centroid = spatial_calculator.calc_spatials(DepthIn, roi)
                        depth = spatials['z']
                        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
                        cv2.putText(frame, f'ID: {id}, Depth: {depth} mm', (x3, y3 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                        cv2.putText(frame, f'X: {spatials["x"]:.2f}, Y: {spatials["y"]:.2f}, Z: {spatials["z"]:.2f}', (x3, y3 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


                cv2.imshow("RGB", frame)

                # depthFrameNorm = cv2.normalize(depthframe, None, 0, 255, cv2.NORM_MINMAX)
                # depthFrameNorm = depthFrameNorm.astype(np.uint8)
                # depthFrameColor = cv2.applyColorMap(depthFrameNorm, cv2.COLORMAP_JET)

                cv2.imshow("Depth", depthFrameColor)

                if cv2.waitKey(1) == ord('q'):
                    break

cv2.destroyAllWindows()
                

                # for name, msg in msgGrp:
                #     frame = msg.getCvFrame()
                #     if name == "disparity":
                #         frame = (frame * disparityMultiplier).astype(np.uint8)
                #         frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
                #         cv2.imshow(name, frame)

                # if cv2.waitKey(1) == ord('q'):
                #        break







        # while True:
        #     inRgb = qRgb.get()  # Recibe el mensaje de GetOuputQueue y espera ell proximo 
        #     msgGrp = qDepth.get()
        #     model(inRgb.getCvFrame(),show=True,device=0)
        #     for name, msg in msgGrp:
        #         frame = msg.getCvFrame()
        #         if name == "disparity":
        #             frame = (frame * disparityMultiplier).astype(np.uint8)
        #             frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
        #             cv2.imshow(name, frame)
        #     if cv2.waitKey(1) == ord("q"):
        #         break

          


