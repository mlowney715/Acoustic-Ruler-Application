#!/usr/bin/python
'''
Acoustic Ruler Control App
Design Project: Team 11 - Abner Barros; Phill Lowney; Alexander Andrade; Nicholas Beckwith
Speech Technology & Applied Research Corp.  Copyright 2016
'''
#Main Window

import wx
import os, sys, inspect,time, datetime, platform, glob, serial

from SC_confdev import SC_confdev

#load config pref. modules from subfolder
configPrefPath = os.path.realpath(
			os.path.abspath
			(
				os.path.join
				(
					os.path.split
					(
						inspect.getfile
						( 
							inspect.currentframe() 
						)
					)
					[0],"configPref"
				)
			)
		)
if configPrefPath not in sys.path:
    sys.path.insert(0, configPrefPath)
    
from configobj import ConfigObj
from wx.lib.pubsub import pub
#from serial.tools import list_ports

######Global Variables#########################################################################################
#Loading preferences from user's preference file
configPref =  ConfigObj()
configPref = ConfigObj('preferences.txt')
speedSound = float(configPref['speed of sound'])
dataLoggerPath = str(configPref['Data path'])

date = datetime.datetime.now()

##############################################################################################################
class EditPreferencesSngChanWindow(wx.Dialog):
    def __init__(self,parent,ID):
        """Constructor"""
        wx.Dialog.__init__(self,parent, ID, "Edit Preferences",size=(670,300),style=wx.MINIMIZE_BOX| wx.CAPTION |wx.CLOSE_BOX)

        self.editPrefWindow() 
#------------------------------------------------------------------------------------------------
    def editPrefWindow(self):
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        
        font_std = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.NORMAL)

        #labels and fields
        str_speedSoundLabel = wx.StaticText(panel, -1, 'Speed of Sound:')
        self.speedSound_txtBox = wx.TextCtrl(panel, wx.ID_ANY, str(speedSound),size=(84,22),style=wx.ALIGN_RIGHT)
        str_speedLabel = wx.StaticText(panel, -1, 'm/s')
        locLabel = wx.StaticText(panel, -1, 'Data Logger Location:')
        self.pathTextBox = wx.TextCtrl(panel, wx.ID_ANY, dataLoggerPath,size=(500,22),style=wx.TE_READONLY|wx.ALIGN_LEFT)
        browseBtn = wx.Button(panel, size=(100,27),label="Browse")
        applyBtn = wx.Button(panel,wx.ID_APPLY, size=(100,27))
        cancelBtn = wx.Button(panel,wx.ID_CANCEL, size=(100,27))
        
        #change fonts & color
        str_speedSoundLabel.SetFont(font_std)
        str_speedLabel.SetFont(font_std)
        self.speedSound_txtBox.SetFont(wx.Font(11,  wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.speedSound_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        self.pathTextBox.SetBackgroundColour(wx.Colour(255,250,250))
        locLabel.SetFont(font_std)
        self.pathTextBox.SetFont(font_std)
        browseBtn.SetFont(font_std)
        applyBtn.SetFont(font_std)
        cancelBtn.SetFont(font_std)

        #binding events for the items
        self.Bind(wx.EVT_CLOSE,self.onClose)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        applyBtn.Bind(wx.EVT_BUTTON, self.onApply)
        browseBtn.Bind(wx.EVT_BUTTON, self.openDir)
        
        #BoxSizer for speed of sound elements
        groupBox_speed = wx.StaticBox(panel, label= 'Edit Speed of Sound')
        groupBox_speed.SetFont(font_std)
        boxsizer_speed = wx.StaticBoxSizer(groupBox_speed, wx.HORIZONTAL)
        boxsizer_speed.Add(str_speedSoundLabel, flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)
        boxsizer_speed.Add(self.speedSound_txtBox, flag=wx.LEFT|wx.TOP, border=10)
        boxsizer_speed.Add(str_speedLabel, flag=wx.TOP|wx.LEFT|wx.ALIGN_LEFT, border=10)

        #gridbag sizer for data logger box sizer
        dataLogGridSizer = wx.GridBagSizer(2,2)
        dataLogGridSizer.Add(locLabel, pos=(0, 0), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        dataLogGridSizer.Add(self.pathTextBox, pos=(1, 0), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        dataLogGridSizer.Add(browseBtn, pos=(1, 1), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)

        #BoxSizer for data logger gridbag
        groupBox_dataLog = wx.StaticBox(panel, label= 'Data Logger')
        groupBox_dataLog.SetFont(font_std)
        boxsizer_dataLog = wx.StaticBoxSizer(groupBox_dataLog, wx.HORIZONTAL)
        boxsizer_dataLog.Add(dataLogGridSizer, flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)

        #gridbag sizer for edit pref.
        editPrefGridSizer = wx.GridBagSizer(3,5)
        editPrefGridSizer.Add(boxsizer_speed, pos=(0, 0),span=(0,4), flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        editPrefGridSizer.Add(boxsizer_dataLog, pos=(1, 0),span=(1,4), flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        editPrefGridSizer.Add(applyBtn, pos=(2, 2), flag=wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT, border=5)
        editPrefGridSizer.Add(cancelBtn, pos=(2, 3), flag=wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM|wx.LEFT, border=5)

        panel.SetSizerAndFit(editPrefGridSizer)
        
#-------------------------------------------------------------------------------------------------------------------
# methods for edit preferences form
    def onClose(self,event):
        self.Destroy()
        event.Skip()
#-------------------------------------------------------------------------------------------------------------------        
    def openDir(self,event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.pathTextBox.SetValue(str(dlg.GetPath()))
        dlg.Destroy()
#-------------------------------------------------------------------------------------------------------------------
    def onApply(self,event):
        global speedSound
        global dataLoggerPath
        speedValue = float(self.speedSound_txtBox.GetValue())
        path = self.pathTextBox.GetValue()

        try:
            configPref['speed of sound'] = str(speedValue)
            configPref['Data path'] = path
            speedSound = speedValue
            dataLoggerPath = path
            configPref.write()
            dataLoggerPath = str(configPref['Data path'])
            speedSound = float(configPref['speed of sound'])
            
            filename = str(dataLoggerPath)+'\SingleChanLog'+str(date.year)+'_'+str(+date.month)+'_'+str(date.day)+'.txt'
            
            if dataLoggerPath is '':
                pub.sendMessage("change_statusbar", msg="Select Logs Directory under 'Edit Preferences'",arg2='RED')
            else:
                if os.path.exists(filename):
                    pub.sendMessage("change_statusbar", msg="Preferences Changed",arg2='DEFAULT')
                    event.Skip()
                else:
                    file = open(filename,'a')
                    pub.sendMessage("change_statusbar", msg="Log file created",arg2='GREEN')
        except ValueError:
            print "error changing preferences"
        self.MakeModal(False)
        self.Close()
        event.Skip()
##############################################################################################################   
##############################################################################################################
class SingleChannelWindow(wx.Frame):
    def __init__(self,parent,ID):
        """Constructor"""
        wx.Frame.__init__(self,parent,ID, "Single Channel System",size=(680,500),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)
        
        self.singleWindow()
#------------------------------------------------------------------------------------------------
    def singleWindow(self):
        
        #Status Bar
        self.statusbar =self.CreateStatusBar()
        
        pub.subscribe(self.change_statusbar,'change_statusbar')
        
        '''Menu Bar '''
        menubar = wx.MenuBar()
        #File
        fileMenu = wx.Menu()
        returnMain = fileMenu.Append(wx.ID_ANY,'&Main Menu','Return to Application Main Menu')
        self.Bind(wx.EVT_MENU, self.returnMainMenu, returnMain)

        qmi = wx.MenuItem(fileMenu,110, '&Quit\tCtrl+Q', 'Quit Application')
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
        
        self.createLog()
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        
        font_std = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_stdBold = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.BOLD)

        #sizer for single channel form
        sizer = wx.GridBagSizer(2,2)
#-------------------------------------------------------------------------------------------------------------------
########Trigger Measurement GroupBox
        trgMeasureGridBag = wx.GridBagSizer(4,8)
        
        trgMeasureStaticBox = wx.StaticBox(panel, label= "Trigger Measurement")
        trgMeasureBoxSizer = wx.StaticBoxSizer(trgMeasureStaticBox, wx.HORIZONTAL)
        
        #buttons,combo box, text boxes & labels (items)
        measureBtn = wx.Button(panel, size=(100,100),label="Measure")
        str_trgChan = wx.StaticText(panel, -1, 'Channel 1 (Speaker 1: Mic 1)')
        distanceLabel = wx.StaticText(panel, -1, 'Distance:')
        distanceTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.metricUnitsComboboxList = ['cm','m']
        self.imperialUnitComboboxList = ['in','ft']
        self.distanceUnitCombobox = wx.ComboBox(panel,-1, size=(80,27),choices=self.metricUnitsComboboxList,style=wx.CB_READONLY)
        self.distanceUnitCombobox.SetValue(self.metricUnitsComboboxList[0])
        self.metricUnitRadioBtn = wx.RadioButton(panel, label = 'Metric', style=wx.RB_GROUP)
        self.metricUnitRadioBtn.SetValue(True)
        self.imperialUnitRadioBtn = wx.RadioButton(panel, label = 'Imperial')
        propTimeLabel = wx.StaticText(panel, -1, 'Propagation Time:')
        propTimeTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        propTimeUnitLabel = wx.StaticText(panel, -1, 'msec')
        gainLabel = wx.StaticText(panel, -1, 'Gain:')
        gainTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        gainUnitLabel = wx.StaticText(panel, -1, '%')

        #change fonts & field color
        trgMeasureStaticBox.SetFont(font_stdBold)
        measureBtn.SetFont(wx.Font(14,  wx.SWISS, wx.NORMAL, wx.BOLD))
        str_trgChan.SetFont(font_stdBold)
        distanceLabel.SetFont(font_std)
        distanceTextBox.SetFont(font_std)
        self.distanceUnitCombobox.SetFont(font_std)
        self.metricUnitRadioBtn.SetFont(font_std)
        self.imperialUnitRadioBtn.SetFont(font_std)
        propTimeLabel.SetFont(font_std)
        propTimeTextBox.SetFont(font_std)
        propTimeUnitLabel.SetFont(font_std)
        gainLabel.SetFont(font_std)
        gainTextBox.SetFont(font_std)
        gainUnitLabel.SetFont(font_std)
        distanceTextBox.SetBackgroundColour(wx.Colour(255,250,250))
        propTimeTextBox.SetBackgroundColour(wx.Colour(255,250,250))
        gainTextBox.SetBackgroundColour(wx.Colour(255,250,250))

        #binding events for the items
        ###Unit of measurement selection for 'distanceUnitCombobox'
        self.metricUnitRadioBtn.Bind(wx.EVT_RADIOBUTTON, self.SetDistanceUnitComboboxVal)
        self.imperialUnitRadioBtn.Bind(wx.EVT_RADIOBUTTON, self.SetDistanceUnitComboboxVal)
        
        #add items to the gridbag
        trgMeasureGridBag.Add(str_trgChan, pos=(0, 0), span=(1,8), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTRE, border=5)
        trgMeasureGridBag.Add(measureBtn, pos=(1, 0), span=(4,3), flag=wx.TOP|wx.LEFT|wx.Right|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(distanceLabel, pos=(1, 3), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(distanceTextBox, pos=(1, 4), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.distanceUnitCombobox, pos=(1, 5), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.metricUnitRadioBtn, pos=(1, 6), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.imperialUnitRadioBtn, pos=(1, 7), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.Right, border=5)
        trgMeasureGridBag.Add(propTimeLabel, pos=(2, 3), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(propTimeTextBox, pos=(2, 4), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(propTimeUnitLabel, pos=(2, 5), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainLabel, pos=(3, 3), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainTextBox, pos=(3, 4), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainUnitLabel, pos=(3, 5), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)

        #add gridbag to the boxsier
        trgMeasureBoxSizer.Add(trgMeasureGridBag, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=10)

########System Status GroupBox
        #Labels
        systemID = wx.StaticText(panel, -1, 'System ID:')
        sysID_field = wx.StaticText(panel, -1, 'AC-0001')
        wiFiStatus = wx.StaticText(panel, -1, 'Status:')
        wiFiStatus_field = wx.StaticText(panel, -1, 'Connected/Disconnected')
        wiFiSSID = wx.StaticText(panel, -1, 'Wi-Fi SSID:')
        wiFiSSID_field = wx.StaticText(panel, -1, 'UMASSD-A')

        #change fonts
        systemID.SetFont(font_stdBold)
        sysID_field.SetFont(font_std)
        wiFiStatus.SetFont(font_stdBold)
        wiFiStatus_field.SetFont(font_std)
        wiFiSSID.SetFont(font_stdBold)
        wiFiSSID_field.SetFont(font_std)

        #gridbag sizer for system status
        sysStatusGridSizer = wx.GridBagSizer(3,3)
        sysStatusGridSizer.Add(systemID, pos=(0, 0), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        sysStatusGridSizer.Add(sysID_field, pos=(0, 2), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM, border=5)
        sysStatusGridSizer.Add(wiFiStatus, pos=(1,0), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        sysStatusGridSizer.Add(wiFiStatus_field, pos=(1,2), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.RIGHT, border=5)
        sysStatusGridSizer.Add(wiFiSSID, pos=(2,0), flag=wx.LEFT|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM, border=5)
        sysStatusGridSizer.Add(wiFiSSID_field, pos=(2,2), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.RIGHT, border=5)

        #Box sizer for system status
        sysStatusStaticBox = wx.StaticBox(panel, label="System Status")
        sysStatusStaticBox.SetFont(font_stdBold)
        sysStatusBoxSizer = wx.StaticBoxSizer(sysStatusStaticBox, wx.HORIZONTAL)
        sysStatusBoxSizer.Add(sysStatusGridSizer, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=25) 

########Configuration GroupBox
        #buttons
        editPrefBtn = wx.Button(panel, size=(160,27),label="Edit Preferences")
        configDeviceBtn = wx.Button(panel, size=(160,27),label="Configure Device")
        searchDeviceBtn = wx.Button(panel, size=(160,27),label="Search for Device")
        
        #change fonts
        editPrefBtn.SetFont(font_std)
        configDeviceBtn.SetFont(font_std)
        searchDeviceBtn.SetFont(font_std)

        #binding events for the buttons
        editPrefBtn.Bind(wx.EVT_BUTTON, self.editPrefBtnClicked)
        configDeviceBtn.Bind(wx.EVT_BUTTON, self.configDeviceBtnClicked)
        searchDeviceBtn.Bind(wx.EVT_BUTTON, self.searchDeviceBtnClicked)

        #Box sizer for config. 
        congfiStaticBox = wx.StaticBox(panel, label='')
        congfiStaticBox.SetFont(font_stdBold)
        configBoxSizer = wx.StaticBoxSizer(congfiStaticBox, wx.VERTICAL)
        configBoxSizer.Add(editPrefBtn, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=20)
        configBoxSizer.Add(configDeviceBtn, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=20)
        configBoxSizer.Add(searchDeviceBtn, flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, border=20)
        
#-------------------------------------------------------------------------------------------------------------------
        #add the 3 main box sizers to the grid sizer for the single channel form
        sizer.Add(trgMeasureBoxSizer, pos=(0, 0),span=(1,2), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM , border=10)
        sizer.Add(sysStatusBoxSizer, pos=(1, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        sizer.Add(configBoxSizer, pos=(1,1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        panel.SetSizerAndFit(sizer)

#-------------------------------------------------------------------------------------------------------------------
# methods for single channel form
    def OnQuit(self, event):
        self.Close()

#-------------------------------------------------------------------------------------------------------------------
    #create log file on opening     
    def createLog(self):
        filename = str(dataLoggerPath)+'\SingleChanLog'+str(date.year)+'_'+str(+date.month)+'_'+str(date.day)+'.txt'
        try:
            if dataLoggerPath is '':
                self.statusbar.SetBackgroundColour('RED')
                self.statusbar.SetStatusText("Select Logs Directory under 'Edit Preferences'")
                self.statusbar.Refresh()
            else:
                if os.path.exists(filename):
                    self.statusbar.SetStatusText('Log file exists')
                    self.statusbar.SetBackgroundColour('YELLOW')
                    wx.FutureCall(8000, self.change_statusbar_to_ready)
                    self.statusbar.Refresh()
                else:
                    file = open(filename,'a')
                    self.statusbar.SetStatusText('Log file created')
                    self.statusbar.SetBackgroundColour('GREEN')
                    wx.FutureCall(8000, self.change_statusbar_to_ready)
                    self.statusbar.Refresh()
        except:
            self.statusbar.SetStatusText('error creating logs')
            self.statusbar.SetBackgroundColour('RED')
#-------------------------------------------------------------------------------------------------------------------
    def change_statusbar(self,msg,arg2=None):
        self.statusbar.SetStatusText(msg)
        if arg2:
            self.statusbar.SetBackgroundColour(arg2)
            self.statusbar.Refresh()
#-------------------------------------------------------------------------------------------------------------------
    def change_statusbar_to_ready(self):
        self.statusbar.SetStatusText('Ready to trigger measurements')
        self.statusbar.SetBackgroundColour('DEFAULT')
        self.statusbar.Refresh()
#-------------------------------------------------------------------------------------------------------------------      
    def returnMainMenu(self, event):
        self.Destroy()
        main_menu = MainWindow(parent=None,ID=999)
        main_menu.Show()
        main_menu.Centre()
#-------------------------------------------------------------------------------------------------------------------
    def SetDistanceUnitComboboxVal(self, event):
        metricState = self.metricUnitRadioBtn.GetValue()
        imperialState = self.imperialUnitRadioBtn.GetValue()

        if imperialState == True:
            self.distanceUnitCombobox.Clear()
            self.distanceUnitCombobox.AppendItems(self.imperialUnitComboboxList)
            self.distanceUnitCombobox.SetValue(self.imperialUnitComboboxList[0])
        elif metricState == True:
            self.distanceUnitCombobox.Clear()
            self.distanceUnitCombobox.AppendItems(self.metricUnitsComboboxList)
            self.distanceUnitCombobox.SetValue(self.metricUnitsComboboxList[0])
#-------------------------------------------------------------------------------------------------------------------
    def editPrefBtnClicked(self, event):
        editPrefFrame = EditPreferencesSngChanWindow(parent=self,ID=997)
        editPrefFrame.Centre()
        editPrefFrame.Show()
        editPrefFrame.ShowModal()
        editPrefFrame.Destroy()
#-------------------------------------------------------------------------------------------------------------------
    def configDeviceBtnClicked(self,event):
        configDevFrame = SC_confdev(parent=self,ID=996)
        configDevFrame.Centre()
        configDevFrame.Show()
        configDevFrame.ShowModal()
        configDevFrame.Destroy()
#-------------------------------------------------------------------------------------------------------------------
    def searchDeviceBtnClicked(self,event):
            bi = wx.BusyInfo("Searching for Device, please wait...", self)
            #**add code here to establish connection with the device over wifi
            time.sleep(10)
            #**creat if-statement to check if device was found or not
            bi2 = wx.BusyInfo("Device found!", self)
            time.sleep(2)
            #**extract information and display them under the system status box
            bi.Destroy()
            bi2.Destroy()
##############################################################################################################            
##############################################################################################################
class MainWindow(wx.Frame):
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
        bmp1 = wx.Bitmap("./ICO/single_channel_button.png", wx.BITMAP_TYPE_ANY)
        singleChanBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp1,size=(bmp1.GetWidth(), bmp1.GetHeight()))
        singleChanBtn.Bind(wx.EVT_BUTTON, self.openSingleChan)

        """Two Channel Button"""
        bmp2 = wx.Bitmap("./ICO/two_channel_button.png", wx.BITMAP_TYPE_ANY)
        twoChanBtn = wx.BitmapButton(panel, id=wx.ID_ANY, bitmap=bmp2,size=(bmp2.GetWidth(), bmp2.GetHeight()))
        #twoChanBtn.Bind(wx.EVT_BUTTON, self.openTwoChan)
        
        """Teamable Button"""
        bmp3 = wx.Bitmap("./ICO/teamable_button.png", wx.BITMAP_TYPE_ANY)
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
        self.Destroy()
        singleChanframe = SingleChannelWindow(parent=None,ID=998)
        singleChanframe.Centre()
        singleChanframe.Show()
##############################################################################################################
##############################################################################################################
if __name__ == '__main__':
    app = wx.App()
    Mainframe = MainWindow(parent=None,ID=999)
    Mainframe.Centre()
    Mainframe.Show()
    app.MainLoop()
