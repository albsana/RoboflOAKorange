import wx
from naranjasFramImpl import naranjasFrameImpl

if __name__ == '__main__':
    wx.SizerFlags.DisableConsistencyChecks()
    app = wx.App()
    fr = naranjasFrameImpl(None)
    fr.Show()
    app.MainLoop()
