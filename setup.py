from mainWindow import mainWindow

import wx

##############################################################################################################
if __name__ == '__main__':
    app = wx.App()
    Mainframe = mainWindow(parent=None,ID=999)
    Mainframe.Centre()
    Mainframe.Show()
    app.MainLoop()
