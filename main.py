import wx
from naranjasFramImpl import naranjasFrameImpl

if __name__ == '__main__':
    wx.SizerFlags.DisableConsistencyChecks()
    app = wx.App()
    fr = naranjasFrameImpl(None)
    fr.Show()
    app.MainLoop()
####
#LD_PRELOAD=/lib/aarch64-linux-gnu/libGLdispatch.so python3 main.py
####
