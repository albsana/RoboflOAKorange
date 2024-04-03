# import cv2

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# writer = cv2.VideoWriter('grabacion.mp4', fourcc, 60.0, (1280,720))
# recording = False

# while True:
#     ret, frame = cap.read()

#     if ret:
#         cv2.imshow('video', frame)
#         if recording: 
#             writer.write(frame)
            
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break
#     elif key == ord('r'):
#         recording = not recording
#         print(f'Recording: {recording}')

# cap.release()
# writer.release()

# cv2.destroyAllWindows()

# #%%

# ###############

                
#                 # if self.naranjaCheckBox.Get3StateValue == True:
#                 #     list_nom.append('Naranja')
#                 # else:
#                 #     if 'Naranja' in list_nom:
#                 #         list_nom.remove('Naranja')

#                 # if self.naranjaVerdeCheckBox.Get3StateValue == True:
#                 #     list_nom.append('NaranjaVerde')
#                 # else:
#                 #     if 'NaranjaVerde' in list_nom:
#                 #         list_nom.remove('NaranjaVerde')


#                 # if list_nom['Naranja'] or list_nom['NaranjaVerde'] in c:
#                 #     list.append([x1,y1,x2,y2])


# list_nom = []
# c = ['Naranja', 'NaranjaVerde', 'Flor']

# list_nom.append('Naranja')

# list_nom.append('NaranjaVerde')
# print(list_nom)

# if c in list_nom:
#     print('1')

# else:
#     print('2')


# # %%
    
# import torch
# from ultralytics import YOLO

# # 加载模型
# model=YOLO(r'C:\Users\Servidor\Desktop\AlbertoMartinez\naranjas\Interfaz\yolov8n_custom20\weights\best.pt')

# # Run batched inference on a list of images
# results = model.predict(0)  # return a list of Results objects

# # Process results list
# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     result.show()  # display to screen
#     result.save(filename='result.jpg')  # save to disk
# # %%
    

# bbox_id=self.tracker.update(list)
# bbox_id1=self.tracker1.update(list1)
# bbox_id2=self.tracker2.update(list2)


# ##############NARANJAS################
# for bbox in bbox_id:
#     x3,y3,x4,y4,id=bbox
#     cx=int(x3+x4)//2
#     cy=int(y3+y4)//2
#     cv2.rectangle(frame, (x3,y3), (x4,y4), (0, 0, 255), 2)

#     if cx1<(cx+offset) and cx1> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
#         oran_pass[id] = cx
#         cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
#         cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
#         counter1.add(id)
#         long1 = len(counter1)

#     if cx2<(cx+offset) and cx2> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
#         oran_pass[id] = cx
#         cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
#         cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
#         counter2.add(id)
#         long2 = len(counter2)

#     if cx3<(cx+offset) and cx3> (cx-offset) and cy1<(cy+offset) and cy2>(cy-offset):
#         oran_pass[id] = cx
#         cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
#         cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
#         counter3.add(id)

#         long3 = len(counter3)

# ################### Segunda imagen ###########################
#     if cx1<(cx+offset) and cx1> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
#         oran_pass[id] = cx
#         cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
#         cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
#         counter4.add(id)
#         long4 = len(counter4)

#     if cx2<(cx+offset) and cx2> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
#         oran_pass[id] = cx
#         cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
#         cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
#         counter5.add(id)
#         long5 = len(counter5)

#     if cx3<(cx+offset) and cx3> (cx-offset) and cy3<(cy+offset) and cy4>(cy-offset):
#         oran_pass[id] = cx
#         cv2.circle(frame,(cx,cy),4,(0,0,255),-1)
#         cv2.putText(frame,str(id),(cx,cy),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,255),2)
#         counter6.add(id)

#         long6 = len(counter6)


# %%
# -*- coding: utf-8 -*-
import wx

class TestFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(200,150))
        self.sz = wx.BoxSizer(wx.VERTICAL)
        
        # Creating controls
        self.red = wx.CheckBox(self, -1, "Red")
        self.green = wx.CheckBox(self, -1, "Green")
        self.blue = wx.CheckBox(self, -1, "Blue")
        
        # Add controls to sizer
        self.sz.Add(self.red, 1, wx.EXPAND|wx.LEFT, 20)
        self.sz.Add(self.green, 1, wx.EXPAND|wx.LEFT, 20)
        self.sz.Add(self.blue, 1, wx.EXPAND|wx.LEFT, 20)
        
        # Bind events
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        
        # Set sizer
        self.SetSizer(self.sz)
        # Centre and show frame
        self.Centre(True)
        self.Show()
        
    def OnCheck(self,event):
        R = float(self.red.GetValue())
        G = float(self.green.GetValue())
        B = float(self.blue.GetValue())
        print(R)
        color = wx.Colour(R*255,G*255,B*255)
        self.SetBackgroundColour(color)
        self.Refresh()
        

if __name__=='__main__':
    app = wx.App()
    frame = TestFrame(None, "wxCheckBox Demo")
    app.MainLoop()
# %%
