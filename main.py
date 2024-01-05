import wx
from naranjasFramImpl import naranjasFrameImpl

if __name__ == '__main__':
    wx.SizerFlags.DisableConsistencyChecks()
    app = wx.App()
    fr = naranjasFrameImpl(None)
    fr.Show()
    app.MainLoop()

    #TEMP
    ####		self.confButtonSpinCtrl1 = wx.SpinCtrlDouble( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0.0, 10, 0 )
    ####		self.confButtonSpinCtrl1.SetIncrement(float(0.01))