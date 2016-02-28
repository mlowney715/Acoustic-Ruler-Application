#!/usr/bin/python
'''
Acoustic Ruler Control App
Design Project: Team 11 - Abner Barros; Phill Lowney; Alexander Andrade; Nicholas Beckwith
Speech Technology & Applied Research Corp.  Copyright 2016
'''
#Main Window

import wx
import os, sys, inspect,time, datetime, platform, glob, serial
from single import (
		single_deviceconf,
		single_window 
		)


#from serial.tools import list_ports

##############################################################################################################
class mainWindow(wx.Frame):
    #function to create window 
    def __init__(self,parent, ID):
        wx.Frame.__init__(self,parent,ID,"Acoustic Ruler Control Application",size=(930,500),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)

        #fixes mismatch between C/C++ and Windows locale
        while str(platform.system()) == 'Windows' or str(platform.system()) == 'Darwin':
            try:
                self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
                break
            except ValueError:
                print "error: mismatch between C/C++ and Windows locale"
        
        self.mainMenu()
#-------------------------------------------------------------------------------------------------
    def mainMenu(self):
        """Panel"""
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        panel.SetBackgroundColour('#f0f0f0')

        """ACOUSTIC RULER TITLE on top"""
        str_AR = wx.StaticText(panel, -1, 'Acoustic Ruler',style=wx.ALIGN_CENTRE)
        font_AR = wx.Font(36,  wx.SWISS, wx.NORMAL, wx.BOLD)
        str_AR.SetFont(font_AR)
        str_AR.SetForegroundColour(wx.Colour(0,102,204))
        
        """VERSION NUMBER"""
        str_verNum = wx.StaticText(panel, -1, 'Version 0.2',style=wx.ALIGN_CENTRE)
        font_verNum = wx.Font(14,  wx.SWISS, wx.NORMAL, wx.NORMAL)
        str_verNum.SetFont(font_verNum)

        """Single Channel Button"""
        bmp1 = wx.Bitmap("./buttons/single_channel_button.png", wx.BITMAP_TYPE_ANY)
        singleChanBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp1,size=(bmp1.GetWidth(), bmp1.GetHeight()))
        singleChanBtn.Bind(wx.EVT_BUTTON, self.openSingleChan)

        """Two Channel Button"""
        bmp2 = wx.Bitmap("./buttons/two_channel_button.png", wx.BITMAP_TYPE_ANY)
        twoChanBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp2,size=(bmp2.GetWidth(), bmp2.GetHeight()))
        #twoChanBtn.Bind(wx.EVT_BUTTON, self.openTwoChan)
        
        """Teamable Button"""
        bmp3 = wx.Bitmap("./buttons/teamable_button.png", wx.BITMAP_TYPE_ANY)
        teamBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp3,size=(bmp3.GetWidth(), bmp3.GetHeight()))
        #teamBtn.Bind(wx.EVT_BUTTON, self.openTeamChan)

        #Button effect on the Mac & Windows
        while str(platform.system()) == 'Windows' or str(platform.system()) == 'Darwin':
            try:
                wx.EVT_ENTER_WINDOW(singleChanBtn, self.OnEnter)
                wx.EVT_LEAVE_WINDOW(singleChanBtn, self.OnLeave)
                wx.EVT_ENTER_WINDOW(twoChanBtn, self.OnEnter)
                wx.EVT_LEAVE_WINDOW(twoChanBtn, self.OnLeave)
                wx.EVT_ENTER_WINDOW(teamBtn, self.OnEnter)
                wx.EVT_LEAVE_WINDOW(teamBtn, self.OnLeave)
                break
            except ValueError:
                print "error changing button cursor for linux OS"
        
        """HELP LINK"""
        str_help = wx.StaticText(panel, -1, 'Help',style=wx.ALIGN_CENTRE)
        font_help = wx.Font(14,  wx.SWISS, wx.NORMAL, wx.NORMAL,underline=True)
        str_help.SetFont(font_help)
        str_help.SetForegroundColour(wx.Colour(0,0,255))
        str_help.SetToolTipString('Open supporting documentation')
        wx.EVT_ENTER_WINDOW(str_help, self.OnEnterHelp)
        str_help.Bind(wx.EVT_LEFT_DOWN, self.openHelp)

        topSizer        = wx.BoxSizer(wx.VERTICAL)
        titleSizer      = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer2     = wx.BoxSizer(wx.HORIZONTAL)
        chnBtnSizer     = wx.BoxSizer(wx.HORIZONTAL)
        titleSizer3     = wx.BoxSizer(wx.HORIZONTAL)

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
#-------------------------------------------------------------------------------------------------
    def OnLeave(self, event):
        btn = event.GetEventObject()
        btn.SetSize(size=(200,200))
#-------------------------------------------------------------------------------------------------
    def OnEnter(self, event):
        btn = event.GetEventObject()
        btn.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        btn.SetSize(size=(201,201))
        
    def OnEnterHelp(self, event):
        btn = event.GetEventObject()
        btn.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
#-------------------------------------------------------------------------------------------------
    def openHelp(self, event):
        '''add another frame/window with help tabs'''
        info = wx.AboutDialogInfo()
        info.SetName('Helpful Documentation coming soon!')
        wx.AboutBox(info)
#------------------------------------------------------------------------------------------------        
    def openSingleChan(self, event):
	    #self.Destroy()
        singleChanframe = single_window(parent=None,ID=998)
        singleChanframe.Centre()
        singleChanframe.Show()
##############################################################################################################
