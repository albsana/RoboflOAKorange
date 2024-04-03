#####################################################################################TIEMPO REAL#########################################################################################


import naranja
import os
import pandas as pd
import wx
import threading
import cv2
import recording
from ultralytics import YOLO
import depthai as dai
import imutils

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
        self.closeButton.Enable()
        self.tracker=Tracker()
        self.tracker1=Tracker()
        self.tracker2=Tracker()
        self.stopVideoFlag = False
        self.filePickerButton.Disable()
        self.naranjaCheckBox.Disable()
        self.naranjaVerdeCheckBox.Disable()

############Variables###############

        self.count=0
        self.cx1=250
        self.cx2=650
        self.cx3=1050
        self.cy1=10
        self.cy2=530
        self.cy3=550
        self.cy4=1070
        self.cVx1=250
        self.cVx2=650
        self.cVx3=1050
        self.cVy1=10
        self.cVy2=530
        self.cVy3=550
        self.cVy4=1070
        self.offset=10
        self.oran_pass={}
        self.green_pass= {}
        self.counter1 = set()
        self.counter2 = set()
        self.counter3 = set()
        self.counter4 = set()
        self.counter5 = set()
        self.counter6 = set()
        self.counterV1 = set()
        self.counterV2 = set()
        self.counterV3 = set()
        self.counterV4 = set()
        self.counterV5 = set()
        self.counterV6 = set()
        self.estimacion = 0
        self.estimacion1 = 0
        self.estimacion2 = 0
        self.estimacionV1 = 0
        self.estimacionV2 = 0
        self.long1 = 0
        self.long2 = 0
        self.long3 = 0
        self.long4 = 0
        self.long5 = 0
        self.long6 = 0
        self.longV1 = 0
        self.longV2 = 0
        self.longV3 = 0
        self.longV4 = 0
        self.longV5 = 0
        self.longV6 = 0

    def naranjaCheckFunc(self, event):

        self.medidasText.Clear()
        if self.naranjaCheckBox.GetValue() == True:
            self.medidasText.AppendText("Activado contar Naranjas")
        else:
            self.medidasText.AppendText("Desactivado contar Naranjas")
        self.Refresh()
        return self.naranjaCheckBox.GetValue()
    
    def naranjaVerdeCheckFunc(self, event):

        self.medidasText.Clear()
        if self.naranjaVerdeCheckBox.GetValue() == True:
            self.medidasText.AppendText("Activado contar Verdes")
        else:
            self.medidasText.AppendText("Desactivado contar Verdes")
        self.Refresh()
        return self.naranjaVerdeCheckBox.GetValue()


    def iniciarProcesoDetectar(self, event):
        self.detectButton.Disable()
        self.stopButton.Enable()
        self.thread = threading.Thread(target=self.detectarRecortar)
        self.thread.start()

    def stopVideo(self):
        if self.stopVideoFlag == True:
            self.closeButton.Enable()
            self.m_choice1.Enable()
            return self.stopVideoFlag

    def cargaModelo(self):
        
        #model=YOLO(r'C:\Users\Servidor\Desktop\AlbertoMartinez\naranjas\Interfaz\yolov8n_custom20\weights\best.pt') #Modelo L Naranajas solo    
        model=YOLO(r'C:\Users\Servidor\Desktop\AlbertoMartinez\NaranjasYOLOv8\runs\detect\naranja_verde4\weights\best.pt') #Modelo custom20 Naranjas y Verdes
        
        return model

    def grabar(self):
        self.closeButton.Disable()
        self.medidasText.Clear()
        self.estimaciontextCtrl.Clear()
        self.medidasText.AppendText("Grabación iniciada...   ")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        writer = cv2.VideoWriter('grabacion.mp4', fourcc, 30.0, (1280,720))
        recording = False

        while True:
            ret, frame = cap.read()
            if not recording:
                cv2.putText(frame, ('Para iniciar grabacion pulse R'), (150, 50), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
                cv2.putText(frame, ('Para detener grabacion pulse R'), (150, 80), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
        
            if ret:
                cv2.imshow('video', frame)
                if recording:
                    writer.write(frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            
            if self.stopVideo() == True:
                break
            
            elif key == ord('r'):
                frame = cv2.putText(frame, '', (0, 0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                recording = not recording
                if recording: 
                    frame = cv2.putText(frame, '', (0, 0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    print(f'Recording: {recording}')
                else: 
                    print(f'Recording: {recording}')
                    

        cap.release()
        writer.release()
        wx.CallAfter(self.detectButton.Enable)
        self.medidasText.AppendText("Finalizado.")
        self.stopVideoFlag = False

        cv2.destroyAllWindows()

    def detectar(self):
        self.closeButton.Disable()
        self.counter1.clear()
        self.counter2.clear()
        self.counter3.clear()
        self.counter4.clear()
        self.counter5.clear()
        self.counter6.clear()
        self.counterV1.clear()
        self.counterV2.clear()
        self.counterV3.clear()
        self.counterV4.clear()
        self.counterV5.clear()
        self.counterV6.clear()
        self.medidasText.Clear()
        self.estimaciontextCtrl.Clear()
        self.medidasText.AppendText("Conteo iniciado...   ")
        modelo = self.cargaModelo()
        naranjaCheck = self.naranjaCheckFunc(event=True)
        naranjaVerdeCheck = self.naranjaVerdeCheckFunc(event=True)
        cx1 = self.cx1
        cx2 = self.cx2
        cx3 = self.cx3
        cy1 = self.cy1
        cy2 = self.cy2
        cy3 = self.cy3
        cy4 = self.cy4
        cVx1 = self.cVx1
        cVx2 = self.cVx2
        cVx3 = self.cVx3
        cVy1 = self.cVy1
        cVy2 = self.cVy2
        cVy3 = self.cVy3
        cVy4 = self.cVy4
        offset = self.offset
        oran_pass = self.oran_pass
        green_pass = self.green_pass 
        counter1 = self.counter1
        counter2 = self.counter2
        counter3 = self.counter3
        counter4 = self.counter4
        counter5 = self.counter5
        counter6 = self.counter6
        counterV1 = self.counterV1
        counterV2 = self.counterV2
        counterV3 = self.counterV3
        counterV4 = self.counterV4
        counterV5 = self.counterV5
        counterV6 = self.counterV6
        estimacion1 = self.estimacion1
        estimacion2 = self.estimacion2
        estimacionV1 = self.estimacionV1
        estimacionV2 = self.estimacionV2
        long1 = self.long1
        long2 = self.long2
        long3 = self.long3
        long4 = self.long4
        long5 = self.long5
        long6 = self.long6
        longV1 = self.longV1
        longV2 = self.longV2
        longV3 = self.longV3
        longV4 = self.longV4
        longV5 = self.longV5
        longV6 = self.longV6

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:

            ret, frame = cap.read()
            print(frame.shape)
            class_list = modelo.names
            results=modelo.predict(frame)
            results[0].conf = 0.35

            a=results[0].boxes.data.cpu()
            px=pd.DataFrame(a).astype("float")
            list=[]
            list1=[]
            list2=[]

            for index,row in px.iterrows():

                x1=int(row[0])
                y1=int(row[1])
                x2=int(row[2])
                y2=int(row[3])
                d=int(row[5])
                c=class_list[d]
                
                if naranjaCheck == True:
                    if 'Naranja' in c:
                        list.append([x1,y1,x2,y2])
                        #self.naranjaCheckBox.Disable()


                elif naranjaVerdeCheck == True: 
                    if 'NaranjaVerde' in c:
                        list1.append([x1,y1,x2,y2])
            
                # elif 'Flor' in c:
                #     list2.append([x1,y1,x2,y2])

                else:
                    print("Nada para predecir")
            bbox_id=self.tracker.update(list)
            bbox_id1=self.tracker1.update(list1)
            #bbox_id2=self.tracker2.update(list2)

######################## NARANJAS ########################
            for bbox in bbox_id:
                x3,y3,x4,y4,id=bbox
                cx=int(x3+x4)//2
                cy=int(y3+y4)//2
                cv2.rectangle(frame, (x3,y3), (x4,y4), (0, 0, 255), 2)

                if cx1<(cx+offset) and cx1> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter1.add(id)
                    long1 = len(counter1)

                if cx2<(cx+offset) and cx2> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter2.add(id)
                    long2 = len(counter2)

                if cx3<(cx+offset) and cx3> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter3.add(id)

                    long3 = len(counter3)

################### Segunda imagen ###########################
                if cx1<(cx+offset) and cx1> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter4.add(id)
                    long4 = len(counter4)

                if cx2<(cx+offset) and cx2> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter5.add(id)
                    long5 = len(counter5)

                if cx3<(cx+offset) and cx3> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter6.add(id)

                    long6 = len(counter6)

######################## NARANJAS VERDES ########################
                    
            for bbox1 in bbox_id1: 
                xV3, yV3, xV4, yV4, idV = bbox1
                cVx = int(xV3 + xV4) // 2
                cVy = int(yV3 + yV4) // 2
                cv2.rectangle(frame, (xV3, yV3), (xV4, yV4), (0, 255, 255))

                if cVx1<(cVx+offset) and cVx1> (cVx-offset) and cVy1<(cVy+offset) and cVy2>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (0, 0, 255), -1)
                    cv2.putText(frame ,str(idV),(cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV1.add(idV)
                    longV1 = len(counterV1)

                if cVx2<(cVx+offset) and cVx2> (cVx-offset) and cVy3<(cVy+offset) and cVy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (0, 0, 255), -1)
                    cv2.putText(frame,str(idV),  (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV2.add(idV)
                    longV2 = len(counterV2)
    
                if cVx3<(cVx+offset) and cVx3> (cVx-offset) and cVy3<(cVy+offset) and cVy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (0, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV3.add(idV)
                    longV3 = len(counterV3)

################### Segunda imagen ###########################
                    

                if cVx1<(cVx+offset) and cVx1> (cVx-offset) and cVy3<(cVy+offset) and cVy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (0, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV1.add(idV)
                    longV4 = len(counterV4)

                if cVx2<(cVx+offset) and cVx2> (cVx-offset) and cVy3<(cVy+offset) and cVy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (0, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV5.add(idV)
                    longV5 = len(counterV5)
    
                if cVx3<(cVx+offset) and cVx3> (cVx-offset) and cVy3<(cVy+offset) and cVy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (0, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV6.add(idV)
                    longV6 = len(counterV6)

######################## --------------- ########################

            cv2.line(frame,(cx1, 350), (cx1, 10),(255,255,255),1)
            cv2.line(frame,(cx2, 350), (cx2, 10),(255,255,255),1)
            cv2.line(frame,(cx3, 350), (cx3, 10),(255,255,255),1)

            cv2.line(frame,(cVx1, 710), (cVx1, 370),(255,255,255),1)
            cv2.line(frame,(cVx2, 710), (cVx2, 370),(255,255,255),1)
            cv2.line(frame,(cVx3, 710), (cVx3, 370),(255,255,255),1)

####################### ESTIMACION NARANJAS ######################

            estimacion1 = (long1 + long2 + long3)/3
            estimacion1 = int(estimacion1)

            estimacion2 = (long4 + long5 + long6 )/3
            estimacion2 = int(estimacion2)

####################### ESTIMACION NARANJAS VERDES ######################
            
            estimacionV1 = (longV1 + longV2 + longV3)/3
            estimacionV1 = int(estimacionV1)

            estimacionV2 = (longV4 + longV5 + longV6 )/3
            estimacionV2 = int(estimacionV2)

########################## ESTIMACION TEXTO #############################

            try:
                self.estimaciontextCtrl.SetValue(f'Linea1:  {long1}\t\t\t\tLinea1 Verdes:  {longV1}\nLinea2:  {long2}\t\t\t\tLinea2 Verdes:  {longV2}\nLinea3:  {long3}\t\t\t\tLinea3 Verdes:  {longV3}\nLinea4:  {long4}\t\t\t\tLinea4 Verdes:  {longV4}\nLinea5:  {long5}\t\t\t\tLinea5 Verdes:  {longV5}\nLinea6:  {long6}\t\t\t\tLinea6 Verdes:  {longV6}\n' 
                                                 + 'Estimación1: ' + str(estimacion1) + '\t\t\t' + 'Estimación Verdes 1: ' + str(estimacionV1) + '\n' + 'Estimacion2: ' + str(estimacion2) + '\t\t\t' + 'Estimación Verdes 2: ' + str(estimacionV2) + '\n'+ 'Estimacion: ' + str(estimacion1+estimacion2) + '\t\t\t' + 'Estimacion Verdes: ' + str(estimacionV1+estimacionV2))
            except RuntimeError:
                self.Close()


            cv2.putText(frame, ('Naranjas: ') + str(estimacion1), (cx1+100, 50), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, ('Naranjas: ') + str(estimacion2), (cx1+100, 400), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)


            cv2.putText(frame, ('Naranjas Verdes: ') + str(estimacionV1), (cVx2+100, 50), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, ('Naranjas Verdes: ') + str(estimacionV2), (cVx2+100, 400), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
    
#########################################################################

            cv2.imshow("RGB", frame)
            if cv2.waitKey(1)&0xFF==27:
                break

            if cv2.waitKey(1) == ord('q'):
                break
            if self.stopVideo() == True:
                break

        cv2.destroyAllWindows()
        os.makedirs(r"C:/Users/Servidor/Desktop/AlbertoMartinez/GUINaranjas/Datos/", exist_ok=True)
        path = r'C:/Users/Servidor/Desktop/AlbertoMartinez/GUINaranjas/Datos/Estimacion.xlsx'
        df = pd.DataFrame({'Estimacion 1' : [long1],
                           'Estimacion 2' : [long2],
                           'Estimacion 3' : [long3],
                           'Estimacion Final' : [estimacion1],})

        if os.path.exists(path):
            df_existe = pd.read_excel(path)
            df = pd.concat([df_existe, df], ignore_index=True)

        df.to_excel(path,index=False)

        wx.CallAfter(self.detectButton.Enable)
        self.medidasText.AppendText("Finalizado.")
        self.stopVideoFlag = False

    def seleccionaCarpeta(self):
        path= self.filePickerButton.GetPath() #Elegir carpeta
        return os.path.join(path)
    
    def selecFunc(self, event):
        
        if self.m_choice1.GetSelection() == 0:
            self.medidasText.Clear()
            self.medidasText.AppendText("Preparado para grabar Video")
            self.naranjaCheckBox.Disable()
            self.naranjaVerdeCheckBox.Disable()

        if self.m_choice1.GetSelection() == 1:
            self.medidasText.Clear()
            self.medidasText.AppendText("Preparado para predecir en tiempo real")
            self.naranjaCheckBox.Enable()
            self.naranjaVerdeCheckBox.Enable()

        if self.m_choice1.GetSelection() == 2:
            self.filePickerButton.Enable()
            self.medidasText.Clear()
            self.medidasText.AppendText("Preparado para predecir en video")
            self.naranjaCheckBox.Enable()
            self.naranjaVerdeCheckBox.Enable()


        else:
            self.filePickerButton.ClearBackground()
            self.filePickerButton.Disable()

    def capturarVideo(self):

        # self.counter1.clear()
        # self.counter2.clear()
        # self.counter3.clear()
        # self.counterV1.clear()
        # self.counterV2.clear()
        # self.counterV3.clear()
        # self.medidasText.Clear()
        # self.estimaciontextCtrl.Clear()
        # self.medidasText.AppendText("Cargando Video...   ")
        # modelo = self.cargaModelo()
        # cap = self.capturarVideo()

        # count = self.count
        # cy1 = self.cy1
        # cy2 = self.cy2
        # cy3 = self.cy3
        # offset = self.offset
        # oran_pass = self.oran_pass
        # green_pass = self.green_pass
        # counter1 = self.counter1
        # counter2 = self.counter2
        # counter3 = self.counter3
        # counterV1 = self.counterV1
        # counterV2 = self.counterV2
        # counterV3 = self.counterV3
        # estimacion = self.estimacion
        # long1 = self.long1
        # long2 = self.long2
        # long3 = self.long3
        # longV1 = self.longV1
        # longV2 = self.longV2
        # longV3 = self.longV3

        # while True:
        #     ret,frame = cap.read()
        #     if not ret:
        #         break
        #     count += 1
        #     if count % 1 != 0:
        #         continue

        #     frame = imutils.resize(frame,width=600)
        #     class_list = modelo.names
        #     results=modelo.predict(frame)
        #     results[0].conf = 0.35

        #     a=results[0].boxes.data.cpu()
        #     px=pd.DataFrame(a).astype("float")
        #     list=[]

        #     for index,row in px.iterrows():

        #         x1=int(row[0])
        #         y1=int(row[1])
        #         x2=int(row[2])
        #         y2=int(row[3])
        #         d=int(row[5])
        #         c=class_list[d]
        #         if 'NaranjaVerde' in c:
        #             list.append([x1,y1,x2,y2])

        #     bbox_id=self.tracker.update(list)
        #     for bbox in bbox_id:
        #         x3,y3,x4,y4,id=bbox
        #         cx=int(x3+x4)//2
        #         cy=int(y3+y4)//2
        #         cv2.rectangle(frame, (x3,y3), (x4,y4), (0, 0, 255), 2)

        #         if cy1<(cx+offset) and cy1> (cx-offset):
        #             oran_pass[id] = cx
        #             cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
        #             cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        #             counter1.add(id)
        #             long1 = len(counter1)

        #         if cy2<(cx+offset) and cy2> (cx-offset):
        #             oran_pass[id] = cx
        #             cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
        #             cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        #             counter2.add(id)
        #             long2 = len(counter2)

        #         if cy3<(cx+offset) and cy3> (cx-offset):
        #             oran_pass[id] = cx
        #             cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
        #             cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
        #             counter3.add(id)

        #             long3 = len(counter3)

        #     # cv2.line(frame,(cy1, 325), (cy1, 10),(255,255,255),1)
        #     # cv2.line(frame,(cy2, 325), (cy2, 10),(255,255,255),1)
        #     # cv2.line(frame,(cy3, 325), (cy3, 10),(255,255,255),1)
        #     cv2.line(frame,(cy1, 1500), (cy1, 10),(255,255,255),1)
        #     cv2.line(frame,(cy2, 1500), (cy2, 10),(255,255,255),1)
        #     cv2.line(frame,(cy3, 1500), (cy3, 10),(255,255,255),1)
        #     # cv2.line(frame,(cy1, 725), (cy1, 10),(255,255,255),1)
        #     # cv2.line(frame,(cy2, 725), (cy2, 10),(255,255,255),1)
        #     # cv2.line(frame,(cy3, 725), (cy3, 10),(255,255,255),1)

        #     # bitmap = wx.StaticBitmap(self.bitmapPanel, wx.ID_ANY, wx.Bitmap(frame))
        #     # bitmap = wx.AnimationCtrl
        #     # bitmap.SetPosition((0,0))

        #     estimacion = (long1 + long2 + long3)/3
        #     estimacion = int(estimacion)
        #     self.estimaciontextCtrl.SetValue(f'Linea1:  {long1}\nLinea2:  {long2}\nLinea3:  {long3}\n' + 'Estimación: ' + str(estimacion))
        #     cv2.putText(frame, ('Naranjas: ') + str(estimacion), (cy1, 50), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
        #     cv2.imshow("RGB", frame)
        #     if cv2.waitKey(1)&0xFF==27:
        #         break

        # cap.release()
        # cv2.destroyAllWindows()
        # os.makedirs(r"F:\Alberto\Interfaz\Datos", exist_ok=True)
        # path = r'F:\Alberto\Interfaz\Datos/Estimacion.xlsx'
        # df = pd.DataFrame({'Estimacion 1' : [long1],
        #                    'Estimacion 2' : [long2],
        #                    'Estimacion 3' : [long3],
        #                    'Estimacion Final' : [estimacion],})

        # if os.path.exists(path):
        #     df_existe = pd.read_excel(path)
        #     df = pd.concat([df_existe, df], ignore_index=True)

        # df.to_excel(path,index=False)

        # #wx.CallAfter(self.bitmap.SetBitmap, frame)
        # wx.CallAfter(self.detectButton.Enable)
        # self.medidasText.AppendText("Finalizado.")

##PREDECIR VIDEO PARA INSTA
        self.closeButton.Disable()
        self.counter1.clear()
        self.counter2.clear()
        self.counter3.clear()
        self.counter4.clear()
        self.counter5.clear()
        self.counter6.clear()
        self.counterV1.clear()
        self.counterV2.clear()
        self.counterV3.clear()
        self.counterV4.clear()
        self.counterV5.clear()
        self.counterV6.clear()
        self.medidasText.Clear()
        self.estimaciontextCtrl.Clear()
        self.medidasText.AppendText("Conteo iniciado...   ")
        modelo = self.cargaModelo()
        naranjaCheck = self.naranjaCheckFunc(event=True)
        naranjaVerdeCheck = self.naranjaVerdeCheckFunc(event=True)
        cx1 = self.cx1
        cx2 = self.cx2
        cx3 = self.cx3
        cy1 = self.cy1
        cy2 = self.cy2
        cy3 = self.cy3
        cy4 = self.cy4
        offset = self.offset
        oran_pass = self.oran_pass
        green_pass = self.green_pass 
        counter1 = self.counter1
        counter2 = self.counter2
        counter3 = self.counter3
        counter4 = self.counter4
        counter5 = self.counter5
        counter6 = self.counter6
        counterV1 = self.counterV1
        counterV2 = self.counterV2
        counterV3 = self.counterV3
        counterV4 = self.counterV4
        counterV5 = self.counterV5
        counterV6 = self.counterV6
        estimacion1 = self.estimacion1
        estimacion2 = self.estimacion2
        estimacionV1 = self.estimacionV1
        estimacionV2 = self.estimacionV2
        long1 = self.long1
        long2 = self.long2
        long3 = self.long3
        long4 = self.long4
        long5 = self.long5
        long6 = self.long6
        longV1 = self.longV1
        longV2 = self.longV2
        longV3 = self.longV3
        longV4 = self.longV4
        longV5 = self.longV5
        longV6 = self.longV6
    
        cap=cv2.VideoCapture(self.seleccionaCarpeta())
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:

            ret, frame = cap.read()

            class_list = modelo.names
            results=modelo.predict(frame)
            results[0].conf = 0.35

            a=results[0].boxes.data.cpu()
            px=pd.DataFrame(a).astype("float")
            list=[]
            list1=[]
            list2=[]

            for index,row in px.iterrows():

                x1=int(row[0])
                y1=int(row[1])
                x2=int(row[2])
                y2=int(row[3])
                d=int(row[5])
                c=class_list[d]
                
                if naranjaCheck == True:
                    if 'Naranja' in c:
                        list.append([x1,y1,x2,y2])
                        #self.naranjaCheckBox.Disable()


                elif naranjaVerdeCheck == True: 
                    if 'NaranjaVerde' in c:
                        list1.append([x1,y1,x2,y2])
            
                # elif 'Flor' in c:
                #     list2.append([x1,y1,x2,y2])

                else:
                    print("Nada para predecir")
            bbox_id=self.tracker.update(list)
            bbox_id1=self.tracker1.update(list1)
            #bbox_id2=self.tracker2.update(list2)

######################## NARANJAS ########################
            for bbox in bbox_id:
                x3,y3,x4,y4,id=bbox
                cx=int(x3+x4)//2
                cy=int(y3+y4)//2
                cv2.rectangle(frame, (x3,y3), (x4,y4), (0, 0, 255), 2)

                if cx1<(cx+offset) and cx1> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter1.add(id)
                    long1 = len(counter1)

                if cx2<(cx+offset) and cx2> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter2.add(id)
                    long2 = len(counter2)

                if cx3<(cx+offset) and cx3> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter3.add(id)

                    long3 = len(counter3)

################### Segunda imagen ###########################
                if cx1<(cx+offset) and cx1> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter4.add(id)
                    long4 = len(counter4)

                if cx2<(cx+offset) and cx2> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter5.add(id)
                    long5 = len(counter5)

                if cx3<(cx+offset) and cx3> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
                    oran_pass[id] = cx
                    cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
                    cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
                    counter6.add(id)

                    long6 = len(counter6)

######################## NARANJAS VERDES ########################
                    
            for bbox1 in bbox_id1: 
                xV3, yV3, xV4, yV4, idV = bbox1
                cVx = int(xV3 + xV4) // 2
                cVy = int(yV3 + yV4) // 2
                cv2.rectangle(frame, (xV3, yV3), (xV4, yV4), (0, 255, 255))

                if cx1<(cVx+offset) and cx1> (cVx-offset) and cy1<(cVy+offset) and cy2>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (255, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV1.add(idV)
                    longV1 = len(counterV1)

                if cx2<(cVx+offset) and cx2> (cVx-offset) and cy3<(cVy+offset) and cy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (255, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV2.add(idV)
                    longV2 = len(counterV2)
    
                if cx3<(cVx+offset) and cx3> (cVx-offset) and cy3<(cVy+offset) and cy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (255, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV3.add(idV)
                    longV3 = len(counterV3)

################### Segunda imagen ###########################
                    

                if cx1<(cVx+offset) and cx1> (cVx-offset) and cy3<(cVy+offset) and cy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (255, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV1.add(idV)
                    longV4 = len(counterV4)

                if cx2<(cVx+offset) and cx2> (cVx-offset) and cy3<(cVy+offset) and cy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (255, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV5.add(idV)
                    longV5 = len(counterV5)
    
                if cx3<(cVx+offset) and cx3> (cVx-offset) and cy3<(cVy+offset) and cy4>(cVy-offset):
                    green_pass[idV] = cVx
                    cv2.circle(frame, (cVx, cVy), 4, (255, 0, 255), -1)
                    cv2.putText(frame,str(idV), (cVx, cVy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    counterV6.add(idV)
                    longV6 = len(counterV6)
######################## --------------- ########################

            cv2.line(frame,(cx1, 350), (cx1, 10),(255,255,255),1)
            cv2.line(frame,(cx2, 350), (cx2, 10),(255,255,255),1)
            cv2.line(frame,(cx3, 350), (cx3, 10),(255,255,255),1)

            cv2.line(frame,(cx1, 710), (cx1, 370),(255,255,255),1)
            cv2.line(frame,(cx2, 710), (cx2, 370),(255,255,255),1)
            cv2.line(frame,(cx3, 710), (cx3, 370),(255,255,255),1)

####################### ESTIMACION NARANJAS ######################

            estimacion1 = (long1 + long2 + long3)/3
            estimacion1 = int(estimacion1)

            estimacion2 = (long4 + long5 + long6 )/3
            estimacion2 = int(estimacion2)

####################### ESTIMACION NARANJAS VERDES ######################
            
            estimacionV1 = (longV1 + longV2 + longV3)/3
            estimacionV1 = int(estimacionV1)

            estimacionV2 = (longV4 + longV5 + longV6 )/3
            estimacionV2 = int(estimacionV2)

########################## ESTIMACION TEXTO #############################

            try:
                self.estimaciontextCtrl.SetValue(f'Linea1:  {long1}\t\t\t\tLinea1 Verdes:  {longV1}\nLinea2:  {long2}\t\t\t\tLinea2 Verdes:  {longV2}\nLinea3:  {long3}\t\t\t\tLinea3 Verdes:  {longV3}\nLinea4:  {long4}\t\t\t\tLinea4 Verdes:  {longV4}\nLinea5:  {long5}\t\t\t\tLinea5 Verdes:  {longV5}\nLinea6:  {long6}\t\t\t\tLinea6 Verdes:  {longV6}\n' 
                                                 + 'Estimación1: ' + str(estimacion1) + '\t\t\t' + 'Estimación Verdes 1: ' + str(estimacionV1) + '\n' + 'Estimacion2: ' + str(estimacion2) + '\t\t\t' + 'Estimación Verdes 2: ' + str(estimacionV2) + '\n'+ 'Estimacion: ' + str(estimacion1+estimacion2) + '\t\t\t' + 'Estimacion Verdes: ' + str(estimacionV1+estimacionV2))
            except RuntimeError:
                self.Close()


            cv2.putText(frame, ('Naranjas: ') + str(estimacion1), (cx1+100, 50), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, ('Naranjas: ') + str(estimacion2), (cx1+100, 400), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)


            cv2.putText(frame, ('Naranjas Verdes: ') + str(estimacionV1), (cx2+100, 50), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
            cv2.putText(frame, ('Naranjas Verdes: ') + str(estimacionV2), (cx2+100, 400), cv2.FONT_ITALIC, 0.8, (0, 255, 255), 2)
    
#########################################################################
            if not ret:
                self.stopVideoFlag = True
                self.stopVideo()
            else:    
                cv2.imshow("RGB", frame)
            if cv2.waitKey(1)&0xFF==27:
                break

            if cv2.waitKey(1) == ord('q'):
                break
            if self.stopVideo() == True:
                break

        cv2.destroyAllWindows()
        os.makedirs(r"C:/Users/Servidor/Desktop/AlbertoMartinez/GUINaranjas/Datos/", exist_ok=True)
        path = r'C:/Users/Servidor/Desktop/AlbertoMartinez/GUINaranjas/Datos/EstimacionGrabacion.xlsx'
        df = pd.DataFrame({'Estimacion 1' : [long1],
                           'Estimacion 2' : [long2],
                           'Estimacion 3' : [long3],
                           'Estimacion Final' : [estimacion1],})

        if os.path.exists(path):
            df_existe = pd.read_excel(path)
            df = pd.concat([df_existe, df], ignore_index=True)

        df.to_excel(path,index=False)

        wx.CallAfter(self.detectButton.Enable)
        self.medidasText.AppendText("Finalizado.")
        self.stopVideoFlag = False

    def seleccion(self):
        #"  " "Grabar" "Predecir Tiempo Real" "Predecir Grabacion" "" ""
        if self.m_choice1.GetSelection() == 0 :
            self.grabar()

        elif self.m_choice1.GetSelection() == 1:
            self.detectar()

        elif self.m_choice1.GetSelection() == 2:
            self.capturarVideo()
###################################
# Botones Main
###################################

    def detectarRecortar(self):
        self.m_choice1.Disable()
        self.seleccion()

    def stopButtonFunc(self, event):
        self.stopVideoFlag = True
        self.stopVideo()

    def closeFunc(self, event):
        self.Close()

###################################
