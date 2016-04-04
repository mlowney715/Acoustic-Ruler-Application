#!/usr/bin/python

"""Acoustic Ruler Control App
Design Project: Team 11 
Abner Barros; Phil Lowney; Alexander Andrade; Nicholas Beckwith
University of Massachusetts Dartmouth
Speech Technology & Applied Research Corp.  Copyright 2016
"""

import wx
import platform
from singleChannel import Single_window, Single_deviceconf, Single_pref


class MainWindow(wx.Frame):
    """Open the Splash Screen for the Acoustic Ruler Program."""

    def __init__(self, parent, ID):
        wx.Frame.__init__(self, parent, ID,
                          "Acoustic Ruler Control Application",
                          size = (930,500),
                          style = wx.MINIMIZE_BOX|
                          wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)

        while (str(platform.system()) == 'Windows' 
               or str(platform.system()) == 'Darwin'):
            try:
                self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
                break
            except ValueError:
                print "Error: Mismatch between C/C++ and Windows locale"
        self.setup()
        
    def setup(self):
        """Create the Splash Screen"""
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        panel.SetBackgroundColour('#f0f0f0')
        str_AR = wx.StaticText(panel, -1, "Acoustic Ruler",
                               style=wx.ALIGN_CENTRE)
        font_AR = wx.Font(36, wx.SWISS, wx.NORMAL, wx.BOLD)
        str_AR.SetFont(font_AR)
        str_AR.SetForegroundColour(wx.Colour(0,102,204))
        str_verNum = wx.StaticText(panel, -1, "Version 0.3",
                                   style=wx.ALIGN_CENTRE)
        font_verNum = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
        str_verNum.SetFont(font_verNum)
        
        # The Single-Channel button opens a SC window.
        bmp1 = wx.Bitmap('./buttons/single_channel_button.png',
                         wx.BITMAP_TYPE_ANY)
        singleChanBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp1,
                                        size=(bmp1.GetWidth(), bmp1.GetHeight()
                                             )
                                       )
        singleChanBtn.Bind(wx.EVT_BUTTON, self.open_SC)

        # The Double-Channel button does nothing.
        bmp2 = wx.Bitmap('./buttons/two_channel_button.png',
                         wx.BITMAP_TYPE_ANY)
        twoChanBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp2,
                                     size=(bmp2.GetWidth(), bmp2.GetHeight()))
        
        # The Teamable-Channel button does nothing.
        bmp3 = wx.Bitmap('./buttons/teamable_button.png', wx.BITMAP_TYPE_ANY)
        teamBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp3,
                                  size=(bmp3.GetWidth(), bmp3.GetHeight()))

        # The following causes animation when hovering over the buttons.
        while (str(platform.system()) == 'Windows'
               or str(platform.system()) == 'Darwin'):
            try:
                wx.EVT_ENTER_WINDOW(singleChanBtn, self.enlarge_btnsize)
                wx.EVT_LEAVE_WINDOW(singleChanBtn, self.reset_btnsize)
                wx.EVT_ENTER_WINDOW(twoChanBtn, self.enlarge_btnsize)
                wx.EVT_LEAVE_WINDOW(twoChanBtn, self.reset_btnsize)
                wx.EVT_ENTER_WINDOW(teamBtn, self.enlarge_btnsize)
                wx.EVT_LEAVE_WINDOW(teamBtn, self.reset_btnsize)
                break
            except ValueError:
                print "error changing button cursor for linux OS"
        
        str_help = wx.StaticText(panel, -1, "Help", style=wx.ALIGN_CENTRE)
        font_help = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL, underline=True)
        str_help.SetFont(font_help)
        str_help.SetForegroundColour(wx.Colour(0,0,255))
        str_help.SetToolTipString("Open supporting documentation")
        wx.EVT_ENTER_WINDOW(str_help, self.hover_help)
        str_help.Bind(wx.EVT_LEFT_DOWN, self.click_help)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        chnBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(str_AR, 0, wx.ALL, 3)
        titleSizer2.Add(str_verNum, 0, wx.ALL, 2)
        chnBtnSizer.Add(singleChanBtn,0,wx.ALL,15)
        chnBtnSizer.Add(twoChanBtn,0,wx.ALL,15)
        chnBtnSizer.Add(teamBtn,0,wx.ALL,15)
        titleSizer3.Add(str_help, 0, wx.ALL,10)

        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(titleSizer2, 0, wx.CENTER)
        topSizer.Add(chnBtnSizer, 0, wx.ALL|wx.CENTER,30)
        topSizer.Add(titleSizer3, 0, wx.ALIGN_RIGHT)

        panel.SetSizer(topSizer)
        topSizer.Fit(self)
        
    def reset_btnsize(self, event):
        """Size the button for when the pointer is not hovering over it."""
        btn = event.GetEventObject()
        btn.SetSize(size=(200,200))
        
    def enlarge_btnsize(self, event):
        """Enlarge the button when the pointer is hovering over it."""
        btn = event.GetEventObject()
        btn.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        btn.SetSize(size=(201,201))
        
    def hover_help(self, event):
        """Change the pointer to a hand when hovering over the help link."""
        btn = event.GetEventObject()
        btn.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        
    def click_help(self, event):
        """Open a help screen when the help link is clicked."""
        info = wx.AboutDialogInfo()
        info.SetName("Acoustic Ruler Program")
        info.AddDeveloper("Acoustic Ruler Team (11): Abner, Phil, Nick, Alex")
        wx.AboutBox(info)
        
    def open_SC(self, event):
        """Launch the Single-Channel window when the SC button is clicked."""
        self.Destroy()
        singleChanframe = Single_window(parent=None, ID=998)
        singleChanframe.Centre()
        singleChanframe.Show()
        
if __name__ == '__main__':
    app = wx.App(redirect=True)
    Mainframe = MainWindow(parent=None,ID=999)
    Mainframe.Centre()
    Mainframe.Show()
    app.MainLoop()
