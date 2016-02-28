import wx
import os 
import platform 
import glob 
import serial
import inspect
import datetime
import time
import sys
import serial

from config import accessconfig

from wx.lib.pubsub import pub
from wifi import Cell

# Global Variables
speedSound, dataLoggerPath = accessconfig()
date = datetime.datetime.now()

##############################################################################################################   
##############################################################################################################
class single_deviceconf(wx.Dialog):
    def __init__(self,parent,ID):

        wx.Dialog.__init__(self,parent, ID, "Configure Device",size=(500,350),style=wx.MINIMIZE_BOX| wx.CAPTION |wx.CLOSE_BOX)

        # Get serial port list on machine
        portList = list(self.serial_ports(self))

	cellList = Cell.all('wlan0')
	ssidList = list()
	count = len(cellList)
	for i in range(0, count-1):
		ssidList.append(cellList[i].ssid)
        # Insert hint for end user
        portList.insert(0, 'Select Board to connect')
        
        self.configDevWindow(ssidList) 
#------------------------------------------------------------------------------------------------
    def configDevWindow(self,myPorts):
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)

        self.font_std = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.NORMAL)

        #labels, fields & buttons
        str_systemAvailable = wx.StaticText(panel, -1, 'System Available:')
        comboBox_sysAvailable = wx.ComboBox(panel,-1, size=(200,27), choices=myPorts, style=wx.CB_READONLY)
        comboBox_sysAvailable.SetSelection(0)
        scanBtn = wx.Button(panel, size=(100,27),label="Scan")
        calibrateSysBtn = wx.Button(panel, size=(145,27),label="Calibrate System")
        configWiFiBtn = wx.Button(panel, size=(130,27),label="Configure Wi-Fi")
        pingBtn = wx.Button(panel, size=(130,27),label="Ping Device")
        closeBtn = wx.Button(panel,wx.ID_CLOSE, size=(100,27))

        #change fonts
        str_systemAvailable.SetFont(self.font_std)
        comboBox_sysAvailable.SetFont(self.font_std)
        scanBtn.SetFont(self.font_std)
        configWiFiBtn.SetFont(self.font_std)
        pingBtn.SetFont(self.font_std)
        calibrateSysBtn.SetFont(self.font_std)
        closeBtn.SetFont(self.font_std)

        #binding events for the items
        self.Bind(wx.EVT_CLOSE,self.onClose)
        closeBtn.Bind(wx.EVT_BUTTON, self.onClose)
        #***bug -> scan button is not function the way is should
        scanBtn.Bind(wx.EVT_BUTTON, self.serial_ports)
        calibrateSysBtn.Bind(wx.EVT_BUTTON, self.startCalibration)

        #box sizer for serial comm.
        serialCommStaticBox = wx.StaticBox(panel,label="Serial Communication")
        serialCommStaticBox.SetFont(self.font_std)
        serialCommBoxSizer = wx.StaticBoxSizer(serialCommStaticBox, wx.HORIZONTAL)
        serialCommBoxSizer.Add(str_systemAvailable, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)
        serialCommBoxSizer.Add(comboBox_sysAvailable, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)
        serialCommBoxSizer.Add(scanBtn, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)

        #box sizer for System Calibration
        sysCalStaticBox = wx.StaticBox(panel,label="System Calibration")
        sysCalStaticBox.SetFont(self.font_std)
        sysCalBoxSizer = wx.StaticBoxSizer(sysCalStaticBox, wx.HORIZONTAL)
        sysCalBoxSizer.Add(calibrateSysBtn, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)

        #box sizer for Wireless Communication
        wifiCommStaticBox = wx.StaticBox(panel,label="Wireless Communication")
        wifiCommStaticBox.SetFont(self.font_std)
        wifiCommBoxSizer = wx.StaticBoxSizer(wifiCommStaticBox, wx.HORIZONTAL)
        wifiCommBoxSizer.Add(configWiFiBtn, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)
        wifiCommBoxSizer.Add(pingBtn, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)

        #gridbag sizer for edit pref.
        configDevGridSizer = wx.GridBagSizer(4,5)
        configDevGridSizer.Add(serialCommBoxSizer, pos=(0, 0),span=(0,4), flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=10)
        configDevGridSizer.Add(sysCalBoxSizer, pos=(1, 0),span=(1,4), flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=10)
        configDevGridSizer.Add(wifiCommBoxSizer, pos=(2, 0),span=(2,4), flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=10)
        configDevGridSizer.Add(closeBtn, pos=(4, 3), flag=wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM|wx.LEFT, border=10)

        panel.SetSizerAndFit(configDevGridSizer)
      
#------------------------------------------------------------------------------------------------
# methods for config. device form
    def onClose(self,event):
        self.Destroy()
        event.Skip()
#------------------------------------------------------------------------------------------------
    def serial_ports(self,event):
	if str(platform.system()) == 'Windows':
		tempList = ['COM%s' % (i + 1) for i in range(256)]
	elif str(platform.system()) == 'Linux':
		tempList = glob.glob('/dev/tty[A-Za-z]*')
	elif str(platform.system()) == 'Darwin':
		tempList = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

        result = []
        for a_port in tempList:
            try:
                s = serial.Serial(a_port)
                s.close()
                result.append(a_port)
            except serial.SerialException:
                pass
        return result
#------------------------------------------------------------------------------------------------
    def startCalibration(self,event):
        message = "Place Microphone as close as possible to speaker.\nClick 'OK' to start system calibration"
        Dlg = wx.MessageDialog(None,message, 'Start System Calibration', wx.OK|wx.CANCEL | wx.ICON_INFORMATION)
        Dlg.SetFont(self.font_std)
        #**create if-statement to check if COM# is selected from the port combobox list
        if Dlg.ShowModal() == wx.ID_OK:
            bi = wx.BusyInfo("Calibrating System, please wait...", self)
            time.sleep(5)
            bi2 = wx.BusyInfo("Done!", self)
            time.sleep(2)
            bi.Destroy()
            bi2.Destroy()
        Dlg.Destroy()
##############################################################################################################
class single_pref(wx.Dialog):
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
	configPref = ConfigObj()
	configPref = ConfigObj('preferences.txt')

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
class single_window(wx.Frame):
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
	# main_menu = mainWindow(parent=None,ID=999)
	# main_menu.Show()
	# main_menu.Centre()
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
        editPrefFrame = single_pref(parent = self, ID = 997)
        editPrefFrame.Centre()
        editPrefFrame.Show()
        editPrefFrame.ShowModal()
        editPrefFrame.Destroy()
#-------------------------------------------------------------------------------------------------------------------
    def configDeviceBtnClicked(self,event):
        configDevFrame = single_deviceconf(parent=self,ID=996)
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
