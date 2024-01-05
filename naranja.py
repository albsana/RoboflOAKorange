# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class naranjaFrame
###########################################################################

class naranjaFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Main", pos = wx.DefaultPosition, size = wx.Size( 652,566 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer68 = wx.BoxSizer( wx.VERTICAL )
		
		self.principal = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer69 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer75 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.principal, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		self.medidasText = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer4.Add( self.medidasText, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer11.Add( sbSizer4, 0, wx.EXPAND, 5 )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self.principal, wx.ID_ANY, u"Imágenes" ), wx.HORIZONTAL )
		
		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer16 = wx.BoxSizer( wx.VERTICAL )
		
		self.confButtonSpinCtrl1 = wx.SpinCtrl( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0, 0, 1, 1 )
		self.confButtonSpinCtrl1.Hide()
		
		bSizer16.Add( self.confButtonSpinCtrl1, 0, wx.ALL, 5 )
		
		self.confianzaCheckBox = wx.CheckBox( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Ver Confianza", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.confianzaCheckBox.SetValue(True) 
		self.confianzaCheckBox.Hide()
		
		bSizer16.Add( self.confianzaCheckBox, 0, wx.ALL, 5 )
		
		self.naranjaCheckBox = wx.CheckBox( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Naranja", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.naranjaCheckBox.Hide()
		
		bSizer16.Add( self.naranjaCheckBox, 0, wx.ALL, 5 )
		
		self.naranjaVerdeCheckBox = wx.CheckBox( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Naranja Verde", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.naranjaVerdeCheckBox.Hide()
		
		bSizer16.Add( self.naranjaVerdeCheckBox, 0, wx.ALL, 5 )
		
		self.florCheckBox = wx.CheckBox( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Flor", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.florCheckBox.Hide()
		
		bSizer16.Add( self.florCheckBox, 0, wx.ALL, 5 )
		
		
		bSizer13.Add( bSizer16, 0, wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Confianza Mínima", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.Hide()
		
		bSizer14.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		
		bSizer13.Add( bSizer14, 0, wx.EXPAND, 5 )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.bitmapPanel = wx.Panel( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.estimaciontextCtrl = wx.TextCtrl( self.bitmapPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		bSizer17.Add( self.estimaciontextCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer17.Add( bSizer26, 1, wx.EXPAND, 5 )
		
		
		self.bitmapPanel.SetSizer( bSizer17 )
		self.bitmapPanel.Layout()
		bSizer17.Fit( self.bitmapPanel )
		bSizer15.Add( self.bitmapPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer13.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		
		sbSizer5.Add( bSizer13, 1, wx.EXPAND, 5 )
		
		bSizer24 = wx.BoxSizer( wx.VERTICAL )
		
		self.detectButton = wx.Button( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Iniciar", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.detectButton.SetFont( wx.Font( 36, 74, 90, 92, False, "Arial Black" ) )
		self.detectButton.SetBackgroundColour( wx.Colour( 1, 214, 12 ) )
		
		bSizer24.Add( self.detectButton, 1, wx.ALL|wx.ALIGN_BOTTOM|wx.EXPAND, 5 )
		
		self.m_panel2 = wx.Panel( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer24.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.stopButton = wx.Button( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Parar", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.stopButton.SetFont( wx.Font( 22, 70, 90, 92, False, "Arial" ) )
		self.stopButton.SetBackgroundColour( wx.Colour( 206, 0, 5 ) )
		
		bSizer24.Add( self.stopButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer27 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.grabacionButton = wx.Button( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Iniciar Grabación", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.grabacionButton.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
		self.grabacionButton.Hide()
		
		bSizer27.Add( self.grabacionButton, 1, wx.ALL, 5 )
		
		self.detenerButton = wx.Button( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Parar Grabación", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.detenerButton.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
		self.detenerButton.Hide()
		
		bSizer27.Add( self.detenerButton, 1, wx.ALL, 5 )
		
		
		bSizer24.Add( bSizer27, 0, wx.EXPAND, 5 )
		
		self.closeButton = wx.Button( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Salir", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.closeButton.SetFont( wx.Font( 16, 74, 90, 90, False, "Arial" ) )
		self.closeButton.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
		
		bSizer24.Add( self.closeButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		sbSizer5.Add( bSizer24, 1, wx.EXPAND, 5 )
		
		
		bSizer11.Add( sbSizer5, 1, wx.EXPAND, 5 )
		
		
		bSizer75.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		
		bSizer69.Add( bSizer75, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.principal, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		self.dirPickerButton = wx.DirPickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		self.dirPickerButton.Hide()
		
		sbSizer1.Add( self.dirPickerButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.filePickerButton = wx.FilePickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		sbSizer1.Add( self.filePickerButton, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer8.Add( sbSizer1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer8, 0, wx.EXPAND, 5 )
		
		
		bSizer69.Add( bSizer7, 0, wx.EXPAND, 5 )
		
		
		self.principal.SetSizer( bSizer69 )
		self.principal.Layout()
		bSizer69.Fit( self.principal )
		bSizer68.Add( self.principal, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer68 )
		self.Layout()
		self.m_menubar2 = wx.MenuBar( 0 )
		self.m_menubar2.Hide()
		
		self.inicioMenu = wx.Menu()
		self.menuPrincipal = wx.MenuItem( self.inicioMenu, wx.ID_ANY, u"Principal", wx.EmptyString, wx.ITEM_NORMAL )
		self.inicioMenu.AppendItem( self.menuPrincipal )
		
		self.panoMenuItem = wx.MenuItem( self.inicioMenu, wx.ID_ANY, u"Panorámica", wx.EmptyString, wx.ITEM_NORMAL )
		self.inicioMenu.AppendItem( self.panoMenuItem )
		
		self.inicioMenu.AppendSeparator()
		
		self.closeMenuItem = wx.MenuItem( self.inicioMenu, wx.ID_ANY, u"Cerrar", wx.EmptyString, wx.ITEM_NORMAL )
		self.inicioMenu.AppendItem( self.closeMenuItem )
		
		self.m_menubar2.Append( self.inicioMenu, u"Inicio" ) 
		
		self.SetMenuBar( self.m_menubar2 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.confButtonSpinCtrl1.Bind( wx.EVT_SPINCTRL, self.spinConfFunc )
		self.confianzaCheckBox.Bind( wx.EVT_CHECKBOX, self.confianzaCheckFunc )
		self.naranjaCheckBox.Bind( wx.EVT_CHECKBOX, self.naranjaCheckFunc )
		self.naranjaVerdeCheckBox.Bind( wx.EVT_CHECKBOX, self.naranjaVerdeCheckFunc )
		self.florCheckBox.Bind( wx.EVT_CHECKBOX, self.florCheckFunc )
		self.detectButton.Bind( wx.EVT_BUTTON, self.detectFunction )
		self.stopButton.Bind( wx.EVT_BUTTON, self.stopButtonFunc )
		self.grabacionButton.Bind( wx.EVT_BUTTON, self.grabacionFunction )
		self.detenerButton.Bind( wx.EVT_BUTTON, self.grabacionStopFunction )
		self.closeButton.Bind( wx.EVT_BUTTON, self.closeFunc )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def spinConfFunc( self, event ):
		event.Skip()
	
	def confianzaCheckFunc( self, event ):
		event.Skip()
	
	def naranjaCheckFunc( self, event ):
		event.Skip()
	
	def naranjaVerdeCheckFunc( self, event ):
		event.Skip()
	
	def florCheckFunc( self, event ):
		event.Skip()
	
	def detectFunction( self, event ):
		event.Skip()
	
	def stopButtonFunc( self, event ):
		event.Skip()
	
	def grabacionFunction( self, event ):
		event.Skip()
	
	def grabacionStopFunction( self, event ):
		event.Skip()
	
	def closeFunc( self, event ):
		event.Skip()
	

###########################################################################
## Class Panoramica
###########################################################################

class Panoramica ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1076,250 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer15 = wx.BoxSizer( wx.VERTICAL )
		
		self.panoPanel = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.panoBitmap = wx.StaticBitmap( self.panoPanel, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.panoBitmap, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.panoPanel.SetSizer( bSizer17 )
		self.panoPanel.Layout()
		bSizer17.Fit( self.panoPanel )
		bSizer15.Add( self.panoPanel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer15, 1, wx.EXPAND, 5 )
		
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel6, wx.ID_ANY, u"Seleccionar Imagen Panorámica" ), wx.VERTICAL )
		
		self.filePickerButtonPano = wx.FilePickerCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		sbSizer11.Add( self.filePickerButtonPano, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer26.Add( sbSizer11, 1, wx.EXPAND, 5 )
		
		
		bSizer19.Add( bSizer26, 0, wx.EXPAND, 5 )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.iniPanoButton = wx.Button( self.m_panel6, wx.ID_ANY, u"Iniciar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer25.Add( self.iniPanoButton, 0, wx.ALL, 5 )
		
		self.m_panel9 = wx.Panel( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer25.Add( self.m_panel9, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.closPanoButton = wx.Button( self.m_panel6, wx.ID_ANY, u"Cerrar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer25.Add( self.closPanoButton, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer25, 0, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer19 )
		self.m_panel6.Layout()
		bSizer19.Fit( self.m_panel6 )
		bSizer18.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer18 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.iniPanoButton.Bind( wx.EVT_BUTTON, self.iniPanoFunc )
		self.closPanoButton.Bind( wx.EVT_BUTTON, self.closePanoFunc )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def iniPanoFunc( self, event ):
		event.Skip()
	
	def closePanoFunc( self, event ):
		event.Skip()
	

###########################################################################
## Class Hiperparametros
###########################################################################

class Hiperparametros ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Parametros", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, u"Valores" ), wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Confidence", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		sbSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		
		bSizer11.Add( sbSizer2, 0, wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, u"label" ), wx.VERTICAL )
		
		
		bSizer11.Add( sbSizer3, 1, wx.EXPAND, 5 )
		
		
		bSizer10.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.acceptParamButton = wx.Button( self.m_panel3, wx.ID_ANY, u"Aceptar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.acceptParamButton, 0, wx.ALL, 5 )
		
		self.m_panel4 = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.closeParamButton = wx.Button( self.m_panel3, wx.ID_ANY, u"Cerrar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.closeParamButton, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer10 )
		self.m_panel3.Layout()
		bSizer10.Fit( self.m_panel3 )
		bSizer9.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.acceptParamButton.Bind( wx.EVT_BUTTON, self.accpetParamFunc )
		self.closeParamButton.Bind( wx.EVT_BUTTON, self.closeParamFunc )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def accpetParamFunc( self, event ):
		event.Skip()
	
	def closeParamFunc( self, event ):
		event.Skip()
	

