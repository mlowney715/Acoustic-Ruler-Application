#!/usr/bin/python
import wx
import os 
import platform 
import glob 
import serial
import datetime
import time
import sys
import serial

from wx.lib.pubsub import pub
from Adata import Adata
from Aserver import Aserver

#create a config. object from Adata
data = Adata('ruler.cfg')

#read speed of sound and datalogger global variables from config.
speedSound = data.speed
dataLoggerPath = data.path

#create a server
#*to be implemeted, retrive this IP when configing the device using serial comm.
#otherwise enter it manually
server = Aserver('10.0.0.3', 12000)

class single_deviceconf(wx.Dialog):
    def __init__(self,parent,ID):
        """Constructor to create a dialog for the single channel device configuration"""
        wx.Dialog.__init__(self,parent, ID, "Configure Device",size=(510,350),
                           style=wx.MINIMIZE_BOX| wx.CAPTION |wx.CLOSE_BOX)

        #Get serial port list on machine
        portList = list(self.serial_ports(self))
        portList.insert(0, 'Select Board to connect')
        '''
        #*once implemented, pass this as an arg. to configDevWindow func. below
        #Scan ang get wifi networks in the surround area
        networkList = list(self.network_ports(self))
        #create a function below called "network_ports" i.e similar to serial_ports
        networkList.insert(0,'Select an Access Point')
        '''
        self.setup(portList)
    #end def
        
    #------------------------------------------------------------------------------------------------
    def setup(self,myPorts):
        '''setup function which takes the serial ports avail. and nets as args.'''
        
        #create a panel for the diaglog
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)

        #font
        self.font_std = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.NORMAL)

        #labels, fields & buttons
        serialSys_label = wx.StaticText(panel, -1, 'System Available:')
        serialSys_comboBox = wx.ComboBox(panel,-1, size=(200,30),
                                         choices=myPorts, style=wx.CB_READONLY)
        serialSys_comboBox.SetSelection(0)
        serialSys_refresh_Btn = wx.Button(panel, size=(100,30),label="Refresh")
        
        network_label = wx.StaticText(panel, -1, 'Choose a Network:')
        network_comboBox = wx.ComboBox(panel,-1, size=(200,30), choices="", style=wx.CB_READONLY)
        network_comboBox.SetSelection(0)
        network_refresh_Btn = wx.Button(panel, size=(100,30),label="Refresh")
        
        password_label = wx.StaticText(panel, -1, 'Password:')
        password_txtBox = wx.TextCtrl(panel, wx.ID_ANY, "",size=(200,27),
                                      style=wx.ALIGN_LEFT|wx.TE_PASSWORD)
        
        pushBtn = wx.Button(panel, size=(130,30),label="Push")
        pingBtn = wx.Button(panel, size=(130,30),label="Ping")
        calibrateSysBtn = wx.Button(panel, size=(130,30),label="Calibrate")
        
        #change fonts
        serialSys_label.SetFont(self.font_std)
        serialSys_comboBox.SetFont(self.font_std)
        serialSys_refresh_Btn.SetFont(self.font_std)
        network_label.SetFont(self.font_std)
        network_comboBox.SetFont(self.font_std)
        network_refresh_Btn.SetFont(self.font_std)
        password_label.SetFont(self.font_std)
        password_txtBox.SetFont(self.font_std)
        pushBtn.SetFont(self.font_std)
        pingBtn.SetFont(self.font_std)
        calibrateSysBtn.SetFont(self.font_std)
        
        #box sizer for serial comm.
        serialCommStaticBox = wx.StaticBox(panel,label="Serial")
        serialCommStaticBox.SetFont(self.font_std)
        serialCommBoxSizer = wx.StaticBoxSizer(serialCommStaticBox, wx.HORIZONTAL)
        serialCommBoxSizer.Add(serialSys_label, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)
        serialCommBoxSizer.Add(serialSys_comboBox, flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=5)
        serialCommBoxSizer.Add(serialSys_refresh_Btn, flag=wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_RIGHT, border=5)

        #gridbag sizer for wireless box sizer
        wirelessGridSizer = wx.GridBagSizer(2,3)
        wirelessGridSizer.Add(network_label, pos=(0, 0), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        wirelessGridSizer.Add(network_comboBox, pos=(0, 1), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        wirelessGridSizer.Add(network_refresh_Btn, pos=(0, 2), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        wirelessGridSizer.Add(password_label, pos=(1,0 ), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)
        wirelessGridSizer.Add(password_txtBox, pos=(1, 1), flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=5)

        #BoxSizer for wireless gridbag
        wirelessGroupBox = wx.StaticBox(panel, label= 'Wireless')
        wirelessGroupBox.SetFont(self.font_std)
        wirelessBoxsizer = wx.StaticBoxSizer(wirelessGroupBox, wx.HORIZONTAL)
        wirelessBoxsizer.Add(wirelessGridSizer, flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=10)
        
        #box sizer for buttons (i.e. push, ping & calibrate)
        btnStaticBox = wx.StaticBox(panel,label="")
        btnStaticBox.SetFont(self.font_std)
        btnBoxSizer = wx.StaticBoxSizer(btnStaticBox, wx.HORIZONTAL)
        btnBoxSizer.Add(pushBtn, flag=wx.LEFT, border=30)
        btnBoxSizer.Add(pingBtn, flag=wx.LEFT|wx.RIGHT, border=10)
        btnBoxSizer.Add(calibrateSysBtn, flag=wx.RIGHT, border=5)
        
        #gridbag sizer ConfigureDeviceSngChanWindow
        configDevGridSizer = wx.GridBagSizer(3,5)
        configDevGridSizer.Add(serialCommBoxSizer, pos=(0, 0),span=(0,4), flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=10)
        configDevGridSizer.Add(wirelessBoxsizer, pos=(1, 0),span=(1,4), flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=10)
        configDevGridSizer.Add(btnBoxSizer, pos=(2, 0),span=(2,4), flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT, border=10)
        panel.SetSizerAndFit(configDevGridSizer)

        #binding events for the items
        self.Bind(wx.EVT_CLOSE,self.onClose)
        #***bug -> scan button is not function the way is should
        calibrateSysBtn.Bind(wx.EVT_BUTTON, self.startCalibration)
    #end def

    #-------------------------------------------------------------------------------------------------------------------
    '''
    The following functions/methods are binded to the items created above 
    '''
    #-------------------------------------------------------------------------------------------------------------------
    #close app. on exit
    def onClose(self,event):
        self.Destroy()
        event.Skip()
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    #search for serial ports on machine
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
    #end def
    
    #-------------------------------------------------------------------------------------------------------------------
    #starts the calibration process
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
    #end def

##############################################################################################################   
##############################################################################################################
class single_pref(wx.Dialog):
    def __init__(self,parent,ID):
        """Constructor to create a dialog for the single channel preferences"""
        wx.Dialog.__init__(self,parent, ID, "Edit Preferences",size=(670,300),
                           style=wx.MINIMIZE_BOX| wx.CAPTION |wx.CLOSE_BOX)

        self.setup()
    #end def
        
    #------------------------------------------------------------------------------------------------
    def setup(self):
        """setup function"""

        #create a panel for the diaglog
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)

        #font style
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

        #binding events for the items
        self.Bind(wx.EVT_CLOSE,self.onClose)
        cancelBtn.Bind(wx.EVT_BUTTON, self.onClose)
        applyBtn.Bind(wx.EVT_BUTTON, self.onApply)
        browseBtn.Bind(wx.EVT_BUTTON, self.openDir)
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    '''
    The following functions/methods are binded to the items created above 
    '''
    #-------------------------------------------------------------------------------------------------------------------
    #close app. on exit
    def onClose(self,event):
        self.Destroy()
        event.Skip()
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    #opens a directory dialog
    def openDir(self,event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.pathTextBox.SetValue(str(dlg.GetPath()))
        dlg.Destroy()
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    #appends changes to the configure file
    def onApply(self,event):
        global speedSound
        global dataLoggerPath

        last_speedSound = speedSound
        filename = str(dataLoggerPath)+"/"+"SingleChannelLog-"+str(datetime.date.today())+".txt"
        
        speedValue = float(self.speedSound_txtBox.GetValue())
        path = self.pathTextBox.GetValue()

        try:
            if speedValue != last_speedSound:
                data.changespeed(speedValue)
                speedSound = speedValue
                data.changespeed(speedSound)
                pub.sendMessage("change_feedTextBox", msg="Speed of Sound changed to: "+str(speedSound)+"m/s\n",arg2='wx.DEFAULT')
            
            dataLoggerPath = path
            data.changepath(dataLoggerPath)
            
            if dataLoggerPath is '':
                pub.sendMessage("change_feedTextBox", msg="Select Logs Directory under 'Edit Preferences'\n",arg2='wx.RED')
            else:
                if os.path.exists(filename):
                    event.Skip()
                else:
                    data.createLogFile()
                    pub.sendMessage("change_feedTextBox", msg="Log file created\n",arg2='wx.GREEN')
        except ValueError:
            pub.sendMessage("change_feedTextBox", msg="error changing preferences\n",arg2='wx.RED')
            
        self.MakeModal(False)
        self.Close()
        event.Skip()
    #end def
        
##############################################################################################################   
##############################################################################################################
class single_window(wx.Frame):
    def __init__(self,parent,ID):
        """Constructor to create a frame for the single channel window"""
        wx.Frame.__init__(self,parent,ID, "Single Channel System",
                          size=(680,650),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)
        
        self.setup()
    #end def
        
    #------------------------------------------------------------------------------------------------
    def setup(self):
        '''setup function for the single channel window'''
        
        #create a statusbar
        self.statusbar =self.CreateStatusBar()
        
        #create a pub subscriber to update the the live feed/logs outside this class
        pub.subscribe(self.change_feedTextBox,'change_feedTextBox')
        
        '''create a Menu Bar'''
        menubar = wx.MenuBar()
        #File
        fileMenu = wx.Menu()
        returnMain = fileMenu.Append(wx.ID_ANY,'&Main Menu','Return to Application Main Menu')
        self.Bind(wx.EVT_MENU, self.returnMainMenu, returnMain)
        #File>quit
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

        #create a panel for the window
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)

        #Fonts
        font_std = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_stdBold = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.BOLD)

        #-------------------------------------------------------------------------------------------------------------------
        '''
        The following blocks are the 4 Group Boxes of the single channel Frame:
        Trigger Measurement; System Status; Configuration; live feed
        At the end of each block the items(i.e. button,textbox) are binded to
        functions which can be triggered by an event(i.e. button clicked).
        '''

        #############################
        #Trigger Measurement GroupBox
        #############################
        
        #buttons,combo box, text boxes & labels (items)
        measureBtn = wx.Button(panel, size=(100,100),label="Measure")
        str_trgChan = wx.StaticText(panel, -1, 'Channel 1 (Speaker 1: Mic 1)')
        distanceLabel = wx.StaticText(panel, -1, 'Distance:')
        self.distanceTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.metricUnitsComboboxList = ['cm','m']
        self.imperialUnitComboboxList = ['in','ft']
        self.distanceUnitCombobox = wx.ComboBox(panel,-1, size=(80,27),choices=self.metricUnitsComboboxList,style=wx.CB_READONLY)
        self.distanceUnitCombobox.SetValue(self.metricUnitsComboboxList[0])
        self.metricUnitRadioBtn = wx.RadioButton(panel, label = 'Metric', style=wx.RB_GROUP)
        self.metricUnitRadioBtn.SetValue(True)
        self.imperialUnitRadioBtn = wx.RadioButton(panel, label = 'Imperial')
        propTimeLabel = wx.StaticText(panel, -1, 'Propagation Time:')
        self.propTimeTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        propTimeUnitLabel = wx.StaticText(panel, -1, 'msec')
        gainLabel = wx.StaticText(panel, -1, 'Gain:')
        gainTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        gainUnitLabel = wx.StaticText(panel, -1, '%')

        #change fonts & field color
        measureBtn.SetFont(wx.Font(14,  wx.SWISS, wx.NORMAL, wx.BOLD))
        str_trgChan.SetFont(font_stdBold)
        distanceLabel.SetFont(font_std)
        self.distanceTextBox.SetFont(font_std)
        self.distanceUnitCombobox.SetFont(font_std)
        self.metricUnitRadioBtn.SetFont(font_std)
        self.imperialUnitRadioBtn.SetFont(font_std)
        propTimeLabel.SetFont(font_std)
        self.propTimeTextBox.SetFont(font_std)
        propTimeUnitLabel.SetFont(font_std)
        gainLabel.SetFont(font_std)
        gainTextBox.SetFont(font_std)
        gainUnitLabel.SetFont(font_std)
        self.distanceTextBox.SetBackgroundColour(wx.Colour(255,250,250))
        self.propTimeTextBox.SetBackgroundColour(wx.Colour(255,250,250))
        gainTextBox.SetBackgroundColour(wx.Colour(255,250,250))
        
        #add items to a gridbag
        trgMeasureGridBag = wx.GridBagSizer(4,8)
        trgMeasureGridBag.Add(str_trgChan, pos=(0, 0), span=(1,8), flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTRE, border=5)
        trgMeasureGridBag.Add(measureBtn, pos=(1, 0), span=(4,3), flag=wx.TOP|wx.LEFT|wx.Right|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(distanceLabel, pos=(1, 3), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.distanceTextBox, pos=(1, 4), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.distanceUnitCombobox, pos=(1, 5), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.metricUnitRadioBtn, pos=(1, 6), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.imperialUnitRadioBtn, pos=(1, 7), flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.Right, border=5)
        trgMeasureGridBag.Add(propTimeLabel, pos=(2, 3), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.propTimeTextBox, pos=(2, 4), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(propTimeUnitLabel, pos=(2, 5), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainLabel, pos=(3, 3), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainTextBox, pos=(3, 4), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainUnitLabel, pos=(3, 5), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)

        #add gridbag to a boxsier
        trgMeasureStaticBox = wx.StaticBox(panel, label= "Trigger Measurement")
        trgMeasureStaticBox.SetFont(font_stdBold)
        trgMeasureBoxSizer = wx.StaticBoxSizer(trgMeasureStaticBox, wx.HORIZONTAL)
        trgMeasureBoxSizer.Add(trgMeasureGridBag, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=10)

        #binding events for the items
        ###Unit of measurement selection for 'distanceUnitCombobox'
        self.metricUnitRadioBtn.Bind(wx.EVT_RADIOBUTTON, self.SetDistanceUnitComboboxVal)
        self.imperialUnitRadioBtn.Bind(wx.EVT_RADIOBUTTON, self.SetDistanceUnitComboboxVal)
        measureBtn.Bind(wx.EVT_BUTTON, self.trig_measure)

        #######################
        #System Status GroupBox
        #######################
        
        #Labels
        systemID = wx.StaticText(panel, -1, 'System ID:')
        sysID_field = wx.StaticText(panel, -1, '--------------------')
        wiFiStatus = wx.StaticText(panel, -1, 'Status:')
        wiFiStatus_field = wx.StaticText(panel, -1, '--------------------')
        wiFiSSID = wx.StaticText(panel, -1, 'Wi-Fi SSID:')
        wiFiSSID_field = wx.StaticText(panel, -1, '--------------------')

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

        #######################
        #Configuration GroupBox
        #######################
        
        #buttons
        editPrefBtn = wx.Button(panel, size=(160,27),label="Edit Preferences")
        configDeviceBtn = wx.Button(panel, size=(160,27),label="Configure Device")
        searchDeviceBtn = wx.Button(panel, size=(160,27),label="Search for Device")
        
        #change fonts
        editPrefBtn.SetFont(font_std)
        configDeviceBtn.SetFont(font_std)
        searchDeviceBtn.SetFont(font_std)

        #Box sizer for config. 
        congfiStaticBox = wx.StaticBox(panel, label='')
        congfiStaticBox.SetFont(font_stdBold)
        configBoxSizer = wx.StaticBoxSizer(congfiStaticBox, wx.VERTICAL)
        configBoxSizer.Add(editPrefBtn, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=20)
        configBoxSizer.Add(configDeviceBtn, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=20)
        configBoxSizer.Add(searchDeviceBtn, flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT, border=20)
        
        #binding events for the buttons
        editPrefBtn.Bind(wx.EVT_BUTTON, self.editPrefBtnClicked)
        configDeviceBtn.Bind(wx.EVT_BUTTON, self.configDeviceBtnClicked)
        searchDeviceBtn.Bind(wx.EVT_BUTTON, self.searchDeviceBtnClicked)

        #######################
        #live feed
        #######################
        
        self.feedTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(500,120),
                                       style=wx.TE_READONLY|wx.ALIGN_LEFT|wx.TE_MULTILINE|wx.TE_RICH2)
        self.feedTextBox.SetFont(font_std)
        self.feedTextBox.SetBackgroundColour(wx.Colour(255,250,250))
        
        #Box sizer for live feed
        feedStaticBox = wx.StaticBox(panel, label='')
        feedStaticBox.SetFont(font_stdBold)
        feedBoxSizer = wx.StaticBoxSizer(feedStaticBox, wx.VERTICAL)
        feedBoxSizer.Add(self.feedTextBox, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=1)

        #call function to create log file after the feed textBox has been created
        self.createLog()

        '''
        Add the 4 box sizers (4 blocks above) to a grid sizer for the single channel frame
        '''
        sizer = wx.GridBagSizer(3,2)
        sizer.Add(trgMeasureBoxSizer, pos=(0, 0),span=(1,2), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM , border=10)
        sizer.Add(sysStatusBoxSizer, pos=(1, 0), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        sizer.Add(configBoxSizer, pos=(1,1), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        sizer.Add(feedBoxSizer, pos=(2,0),span=(1,2), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT , border=10)
        panel.SetSizerAndFit(sizer)
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    '''
    The following functions/methods are binded to the items created above 
    '''
    #-------------------------------------------------------------------------------------------------------------------
    #close app. on exit
    def OnQuit(self, event):
        self.Close()
        server.closeSocket()
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    #create log file on opening if a path is already specified     
    def createLog(self):
        filename = str(dataLoggerPath)+"/"+"SingleChannelLog-"+str(datetime.date.today())+".txt"
        try:
            if dataLoggerPath is '':
                self.feedTextBox.SetDefaultStyle(wx.TextAttr(wx.BLACK,wx.RED))
                self.feedTextBox.AppendText("!Select Logs Directory under 'Edit Preferences'\n")
            else:
                if os.path.exists(filename):
                    self.feedTextBox.SetDefaultStyle(wx.TextAttr(wx.BLACK,wx.YELLOW))
                    self.feedTextBox.AppendText("Log file exists\n")
                else:
                    data.createLogFile()
                    self.feedTextBox.SetDefaultStyle(wx.TextAttr(wx.GREEN))
                    self.feedTextBox.AppendText("Log file created\n")
        except:
            self.feedTextBox.SetDefaultStyle(wx.TextAttr(wx.BLACK,wx.RED))
            self.feedTextBox.AppendText("!Error creating logs\n")
    #end def
            
    #-------------------------------------------------------------------------------------------------------------------
    #function called by the pub subscriber to append text to the live feed/log
    def change_feedTextBox(self,msg,arg2=None):
        self.feedTextBox.AppendText(msg)
        if arg2:
            self.feedTextBox.SetDefaultStyle(wx.TextAttr(arg2))
    #end def
            
    #-------------------------------------------------------------------------------------------------------------------
    #called from the menybar File > Return to Main Menu 
    def returnMainMenu(self, event):
        #to be implemented (work around, since parent(setup.py) cant be imported)
        self.Destroy()
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    '''
    Sets the correct unit of measurment on the distance Unit Combobox when
    metric and imperial radio buttons are toggled.
    carries out conversion when radio buttons are toggled and unit of measurement
    are changed.
    '''
    def SetDistanceUnitComboboxVal(self, event):
        metricState = self.metricUnitRadioBtn.GetValue()
        imperialState = self.imperialUnitRadioBtn.GetValue()
        
        if self.distanceTextBox.GetValue() != "":
            last_value = float(self.distanceTextBox.GetValue())
        last_unitComboboxValue = self.distanceUnitCombobox.GetValue()
        
        if imperialState == True:
            self.distanceUnitCombobox.Clear()
            self.distanceUnitCombobox.AppendItems(self.imperialUnitComboboxList)
            self.distanceUnitCombobox.SetValue(self.imperialUnitComboboxList[0])
        elif metricState == True:
            self.distanceUnitCombobox.Clear()
            self.distanceUnitCombobox.AppendItems(self.metricUnitsComboboxList)
            self.distanceUnitCombobox.SetValue(self.metricUnitsComboboxList[0])
            
        current_unitComboboxValue = self.distanceUnitCombobox.GetValue()

        if self.distanceTextBox.GetValue() != "":
            if last_unitComboboxValue == "cm" and current_unitComboboxValue == "in":
                self.distanceTextBox.SetValue(str((last_value)/2.54))
            elif last_unitComboboxValue == "cm" and current_unitComboboxValue == "ft":
                self.distanceTextBox.SetValue(str((last_value)* 0.032808))
            elif last_unitComboboxValue == "m" and current_unitComboboxValue == "in":
                self.distanceTextBox.SetValue(str((last_value)* 39.370))
            elif last_unitComboboxValue == "m" and current_unitComboboxValue == "ft":
                self.distanceTextBox.SetValue(str((last_value)/0.3048))

            elif last_unitComboboxValue == "in" and current_unitComboboxValue == "cm":
                self.distanceTextBox.SetValue(str((last_value)*2.54))
            elif last_unitComboboxValue == "in" and current_unitComboboxValue == "m":
                self.distanceTextBox.SetValue(str((last_value)/39.370))
            elif last_unitComboboxValue == "ft" and current_unitComboboxValue == "cm":
                self.distanceTextBox.SetValue(str((last_value)/0.032808))
            elif last_unitComboboxValue == "ft" and current_unitComboboxValue == "m":
                self.distanceTextBox.SetValue(str((last_value)/3.2808))
    #end def
            
    #-------------------------------------------------------------------------------------------------------------------
    #launches the single changle preferences dialog/window
    def editPrefBtnClicked(self, event):
        editPrefFrame = single_pref(parent = self, ID = 997)
        editPrefFrame.Centre()
        editPrefFrame.Show()
        editPrefFrame.ShowModal()
        editPrefFrame.Destroy()
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    #launches the single changle device configuration dialog/window
    def configDeviceBtnClicked(self,event):
        configDevFrame = single_deviceconf(parent=self,ID=996)
        configDevFrame.Centre()
        configDevFrame.Show()
        configDevFrame.ShowModal()
        configDevFrame.Destroy()
    #end def
 
    #-------------------------------------------------------------------------------------------------------------------
    #search for device after configured
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
    #end def

    #-------------------------------------------------------------------------------------------------------------------
    #triggers a measurement using the server, then display the distance and time delays
    def trig_measure(self,event):
        global speedSound
        unitComboboxValue = self.distanceUnitCombobox.GetValue()
        
        delay = server.getdelay()
        data.measure(delay)
        
        if unitComboboxValue == "m":
            self.distanceTextBox.SetValue('{:0.2f}'.format(delay*speedSound))
        elif unitComboboxValue == "cm":
            self.distanceTextBox.SetValue('{:0.2f}'.format((delay*speedSound)*100))
        elif unitComboboxValue == "in":
            self.distanceTextBox.SetValue('{:0.2f}'.format((delay*speedSound)*39.370))
        elif unitComboboxValue == "ft":
            self.distanceTextBox.SetValue('{:0.2f}'.format((delay*speedSound)/0.3048))
        
        self.distanceTextBox.SetValue(str(delay*speedSound))
        self.propTimeTextBox.SetValue(str(delay*1000.0))

        #phil, test the timeout for the server script/module when the ip is not configured
        '''
        try: 
            delay = server.getdelay()
            data.measure(delay)
            if unitComboboxValue == "m":
                self.distanceTextBox.SetValue(str(delay*speedSound))
            elif unitComboboxValue == "cm":
                self.distanceTextBox.SetValue(str((delay*speedSound)*100))
            elif unitComboboxValue == "in":
                self.distanceTextBox.SetValue(str((delay*speedSound)*39.370))
            elif unitComboboxValue == "ft":
                self.distanceTextBox.SetValue(str((delay*speedSound)/0.3048))
        
            self.distanceTextBox.SetValue(str(delay*speedSound))
            self.propTimeTextBox.SetValue(str(delay*1000.0))
        except ServerError:
            print "Error connecting to device"
        '''
    #end def
        
    #-------------------------------------------------------------------------------------------------------------------
    #to be implemented, update distance value when user switch bewtween the dist. unit comboBox i.e. from cm to m
    def updateDistTextBox(self,last_val):
        last_value = self.distanceTextBox.GetValue()
        last_unitComboboxValue = last_val
        current_unitComboboxValue = self.distanceUnitCombobox.GetValue()
        
        if last_unitComboboxValue == "cm" and current_unitComboboxValue == "m":
            self.distanceTextBox.SetValue(str((last_value)/100.0))
        elif last_unitComboboxValue == "m" and current_unitComboboxValue == "cm":
            self.distanceTextBox.SetValue(str((last_value)*100.0))
            
        elif last_unitComboboxValue == "in" and current_unitComboboxValue == "ft":
            self.distanceTextBox.SetValue(str((last_value)*0.083333))
        elif last_unitComboboxValue == "ft" and current_unitComboboxValue == "in":
            self.distanceTextBox.SetValue(str((last_value)*12.000))
    #end def
