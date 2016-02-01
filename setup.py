#!/usr/bin/python
#'''
#Acoustic Ruler Control App
#Design Project: Team 11 - Abner Barros; Phill Lowney; Alexander Andrade; Nicholas Beckwith
#Speech Technology & Applied Research Corp.  Copyright 2016
#'''

#Main Window

import wx
import os

class SingleChannelWindow(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self,None, wx.ID_ANY, "Single Channel System",size=(1000,700))

        ######Global Variables##########
        self.speedSound = 343.2 #m/s
        ################################
    
        self.singleWindow()
        self.Centre()
        self.Show() 
#------------------------------------------------------------------------------------------------
    def singleWindow(self):

        #Status Bar
        self.CreateStatusBar()
        self.SetStatusText('Ready to trigger measurements')

        '''Menu Bar '''
        menubar = wx.MenuBar()
        #File
        fileMenu = wx.Menu()
        returnMain = fileMenu.Append(wx.ID_ANY,'&Main Menu')
        self.Bind(wx.EVT_MENU, self.returnMainMenu, returnMain)
        #fix event handle below
        self.Bind(wx.EVT_MENU_OPEN, self.OnMainMenu)

        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
        #Edit
        editMenu = wx.Menu()
        #Options
        optionsMenu = wx.Menu()
        optionsMenu.Append(wx.ID_ANY,'&Configure Wi-Fi')
        optionsMenu.Append(wx.ID_ANY,'&Calibrate System')
        #Help
        helpMenu = wx.Menu()
        helpMenu.Append(wx.ID_ANY,'&About')

        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(optionsMenu, '&Options')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)
#------------------------------------------------------------------------------------------------------------------------------------------
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        
        sizer = wx.GridBagSizer(3,2)
        sizer_groupBox1 = wx.GridBagSizer(4,5)
        
########Trigger Measurement GroupBox
        font_std = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_stdBold = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.BOLD)

        triggerBtn = wx.Button(panel, size=(100,100),label="Trigger")
        triggerBtn.SetFont(wx.Font(14,  wx.SWISS, wx.NORMAL, wx.BOLD))
        
        str_trgChan = wx.StaticText(panel, -1, 'Channel 1 (Speaker 1: Mic 1)')
        str_trgChan.SetFont(font_stdBold)
        cm_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)             #***set calc value to here***
        cm_txtBox.SetFont(wx.Font(11,  wx.SWISS, wx.NORMAL, wx.NORMAL))
        cm_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        str_cmLabel = wx.StaticText(panel, -1, 'cm')
        str_cmLabel.SetFont(font_std)
        in_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)             #***set calc value to here***
        in_txtBox.SetFont(wx.Font(11,  wx.SWISS, wx.NORMAL, wx.NORMAL))
        in_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        str_inLabel = wx.StaticText(panel, -1, 'in')
        str_inLabel.SetFont(font_std)
        str_speedSoundLabel = wx.StaticText(panel, -1, 'Speed of Sound:')
        str_speedSoundLabel.SetFont(font_std)
        self.speedSound_txtBox = wx.TextCtrl(panel, wx.ID_ANY, str(self.speedSound),size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)  #***Get speed of sound value from here***
        self.speedSound_txtBox.SetFont(wx.Font(11,  wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.speedSound_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        str_speedLabel = wx.StaticText(panel, -1, 'm/s')
        str_speedLabel.SetFont(font_std)
        editSpeedBtn = wx.Button(panel, size=(112,27),label="Edit")
        editSpeedBtn.SetFont(font_std)
        editSpeedBtn.Bind(wx.EVT_BUTTON, self.editSpeedSound)

        groupBox1 = wx.StaticBox(panel, label= "Trigger Measurement")
        groupBox1.SetFont(font_stdBold)
        boxsizer_trgMeasure = wx.StaticBoxSizer(groupBox1, wx.HORIZONTAL)

        #BoxSizer for speed of sound elements
        groupBox_speed = wx.StaticBox(panel, label= '')
        boxsizer_speed = wx.StaticBoxSizer(groupBox_speed, wx.HORIZONTAL)
        boxsizer_speed.Add(str_speedSoundLabel, flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)
        boxsizer_speed.Add(self.speedSound_txtBox, flag=wx.LEFT|wx.TOP, border=10)
        boxsizer_speed.Add(str_speedLabel, flag=wx.TOP|wx.LEFT|wx.ALIGN_LEFT, border=10)
        boxsizer_speed.Add(editSpeedBtn, flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.RIGHT, border=10)


        ###GridBagSizer for ENTIRE Trigger Measurement Groupbox elements
        sizer_groupBox1.Add(triggerBtn, pos=(0, 0), span=(4,2), flag=wx.TOP|wx.LEFT, border=5)
        sizer_groupBox1.Add(str_trgChan, pos=(0, 2),span=(1,5), flag=wx.TOP|wx.ALIGN_CENTRE|wx.RIGHT, border=5)
        
        sizer_groupBox1.Add(cm_txtBox, pos=(1, 2),  flag=wx.TOP|wx.LEFT|wx.ALIGN_CENTRE, border=20)
        sizer_groupBox1.Add(str_cmLabel, pos=(1, 3), flag=wx.TOP|wx.ALIGN_CENTRE, border=20)
        sizer_groupBox1.Add(in_txtBox, pos=(1, 4), flag=wx.TOP|wx.LEFT|wx.ALIGN_RIGHT, border=20)
        sizer_groupBox1.Add(str_inLabel, pos=(1, 5), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, border=20) #flag=wx.TOP|wx.LEFT|wx.BOTTOM
        
        sizer_groupBox1.Add(boxsizer_speed, pos=(4, 0),span=(4,5), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)

        #add Gridbagsizer trigger elements to the Trigger Measurement GroupBox boxsizer
        boxsizer_trgMeasure.Add(sizer_groupBox1, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=10)

########Configuration GroupBox
        #buttons and labels
        str_systemAvailable = wx.StaticText(panel, -1, 'System Available:')
        sysAvailable_combobox_list = ['pyBoard1','pyBoard2','pyBoard3']
        comboBox_sysAvailable = wx.ComboBox(panel,-1, size=(130,27), choices=sysAvailable_combobox_list, style=wx.CB_READONLY)
        refreshBtn = wx.Button(panel, size=(27,27),label="R")
        configWiFiBtn = wx.Button(panel, size=(130,27),label="Configure Wi-Fi")
        pingBtn = wx.Button(panel, size=(130,27),label="Ping")
        configBoxLine = wx.StaticLine(panel)
        searchDeviceBtn = wx.Button(panel, size=(145,27),label="Search for Device")
        calibrateSysBtn = wx.Button(panel, size=(145,27),label="Calibrate System")

        #change fonts
        str_systemAvailable.SetFont(font_std)
        comboBox_sysAvailable.SetFont(font_std)
        refreshBtn.SetFont(font_std)
        configWiFiBtn.SetFont(font_std)
        pingBtn.SetFont(font_std)
        searchDeviceBtn.SetFont(font_std)
        calibrateSysBtn.SetFont(font_std)


        #gridbag sizer for serial comm. elements
        serialCommGridSizer = wx.GridBagSizer(2,3)
        serialCommGridSizer.Add(str_systemAvailable, pos=(0, 0), flag=wx.TOP|wx.ALIGN_LEFT, border=5)
        serialCommGridSizer.Add(comboBox_sysAvailable, pos=(0, 1), flag=wx.TOP|wx.ALIGN_CENTRE, border=5)
        serialCommGridSizer.Add(refreshBtn, pos=(0, 2), flag=wx.TOP|wx.RIGHT, border=5)
        serialCommGridSizer.Add(configWiFiBtn, pos=(1, 0), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM, border=10)
        serialCommGridSizer.Add(pingBtn, pos=(1, 1), flag=wx.TOP|wx.ALIGN_CENTRE|wx.BOTTOM, border=10)

        #box sizer for serial comm.
        serialCommStaticBox = wx.StaticBox(panel,label="")
        serialCommBoxSizer = wx.StaticBoxSizer(serialCommStaticBox, wx.HORIZONTAL)
        serialCommBoxSizer.Add(serialCommGridSizer, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)
    
        #gridbag sizer for wi-fi comm.
        wiFiCommGridSizer = wx.GridBagSizer(1,3)
        wiFiCommGridSizer.Add(searchDeviceBtn, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        wiFiCommGridSizer.Add(calibrateSysBtn, pos=(0, 1), flag=wx.TOP|wx.RIGHT|wx.BOTTOM, border=5)

        #box sizer for wi-fi comm.
        wiFiCommStaticBox = wx.StaticBox(panel,label="")
        wiFiCommBoxSizer = wx.StaticBoxSizer(wiFiCommStaticBox, wx.HORIZONTAL)
        wiFiCommBoxSizer.Add(wiFiCommGridSizer, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)

        #gridbag sizer for box sizers (serial comm. & wi-fi comm.)
        configGridSizer = wx.GridBagSizer(1,2)
        configGridSizer.Add(serialCommBoxSizer, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTRE, border=5)
        configGridSizer.Add(configBoxLine, pos=(1, 0), border=5)
        configGridSizer.Add(wiFiCommBoxSizer, pos=(2, 0), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTRE, border=5)

        
        groupBox2 = wx.StaticBox(panel, label="Configuration")
        groupBox2.SetFont(font_stdBold)
        boxsizer_config = wx.StaticBoxSizer(groupBox2, wx.HORIZONTAL)
        boxsizer_config.Add(configGridSizer, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=10)
        
        #boxsizer2.Add(wx.CheckBox(panel, label="Generate Default Constructor"), flag=wx.LEFT|wx.TOP, border=10)

########System Status GroupBox
        groupBox3 = wx.StaticBox(panel, label="Config")
        boxsizer3 = wx.StaticBoxSizer(groupBox3, wx.HORIZONTAL)
        boxsizer3.Add(wx.CheckBox(panel, label="Generate Main Method"), flag=wx.LEFT|wx.TOP, border=10)

########System Status GroupBox
        groupBox5 = wx.StaticBox(panel, label="Config")
        boxsizer5 = wx.StaticBoxSizer(groupBox5, wx.HORIZONTAL)
        boxsizer5.Add(wx.CheckBox(panel, label="Public"), flag=wx.LEFT|wx.TOP, border=10)
#-------------------------------------------------------------------------------------------------------------------
        sizer.Add(boxsizer_trgMeasure, pos=(0, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM , border=10) #add boxSizer to bagsizer
        sizer.Add(boxsizer_config, pos=(0, 1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        sizer.Add(boxsizer3, pos=(1, 0),span=(1,2), flag=wx.EXPAND|wx.LEFT|wx.RIGHT , border=10)
        sizer.Add(boxsizer5, pos=(2, 0),span=(1,2), flag=wx.EXPAND|wx.LEFT|wx.RIGHT , border=10)
        panel.SetSizerAndFit(sizer)
       
#-----------------------------------------------------------------------------------------------
    def OnMainMenu(self, event):
        self.SetStatusText('Return To Main Menu')
    def OnQuit(self, event):
        self.Close()
#-------------------------------------------------------------------------------------------------------------------
    def returnMainMenu(self, event):
        self.Destroy()
        main_menu = MainWindow(None,title='Acoustic Ruler Control Application')
        main_menu.Show()
#-------------------------------------------------------------------------------------------------------------------
    def editSpeedSound(self, event):
        dlg = wx.TextEntryDialog(self, 'Enter speed of sound','Edit Speed of Sound')
        dlg.SetValue(str(self.speedSound))
        if dlg.ShowModal() == wx.ID_OK:
            self.speedSound = float(dlg.GetValue())
            self.speedSound_txtBox.SetValue(dlg.GetValue())
            self.SetStatusText('You have changed the speed of sound to: %s\n m/s' %dlg.GetValue())
        dlg.Destroy()
            
##################################################################################################
class MainWindow(wx.Frame):
    #function to create window 
    def __init__(self,parent, title):
        super(MainWindow, self).__init__(parent,title=title, size=(930, 500),style=wx.MINIMIZE_BOX
	| wx.SYSTEM_MENU | wx.CAPTION |	 wx.CLOSE_BOX)
        #   self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.frame = parent
        
        self.mainMenu()
        self.Centre()
        self.Show()
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
        str_verNum = wx.StaticText(panel, -1, 'Version 0.1',style=wx.ALIGN_CENTRE)
        font_verNum = wx.Font(14,  wx.SWISS, wx.NORMAL, wx.NORMAL)
        str_verNum.SetFont(font_verNum)
        
        """Single Channel Button"""
        bmp1 = wx.Bitmap("./ICO/single_channel_button.png", wx.BITMAP_TYPE_ANY)
        singleChanBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp1,size=(bmp1.GetWidth(), bmp1.GetHeight()))
        #wx.EVT_ENTER_WINDOW(singleChanBtn, self.OnEnter)
        #wx.EVT_LEAVE_WINDOW(singleChanBtn, self.OnLeave)
        singleChanBtn.Bind(wx.EVT_BUTTON, self.openSingleChan)
        
        """Two Channel Button"""
        bmp2 = wx.Bitmap("./ICO/two_channel_button.png", wx.BITMAP_TYPE_ANY)
        twoChanBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp2,size=(bmp2.GetWidth(), bmp2.GetHeight()))
        wx.EVT_ENTER_WINDOW(twoChanBtn, self.OnEnter)
        wx.EVT_LEAVE_WINDOW(twoChanBtn, self.OnLeave)
        
        """Teamable Button"""
        bmp3 = wx.Bitmap("./ICO/teamable_button.png", wx.BITMAP_TYPE_ANY)
        teamBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp3,size=(bmp3.GetWidth(), bmp3.GetHeight()))
        wx.EVT_ENTER_WINDOW(teamBtn, self.OnEnter)
        wx.EVT_LEAVE_WINDOW(teamBtn, self.OnLeave)
        
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
        self.Destroy()
        new_frame = SingleChannelWindow()
        new_frame.Show()

#################################################################################################
if __name__ == '__main__':

    app = wx.App()
    MainWindow(None,title='Acoustic Ruler Control Application')
    app.MainLoop()
