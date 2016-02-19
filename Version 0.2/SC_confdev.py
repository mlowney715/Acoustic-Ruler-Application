import wx
import os, platform, glob, serial

##############################################################################################################   
##############################################################################################################
class SC_confdev(wx.Dialog):
    def __init__(self,parent,ID):

        wx.Dialog.__init__(self,parent, ID, "Configure Device",size=(500,350),style=wx.MINIMIZE_BOX| wx.CAPTION |wx.CLOSE_BOX)

        # Get serial port list on machine
        portList = list(self.serial_ports(self))

        # Insert hint for end user
        portList.insert(0, 'Select Board to connect')
        
        self.configDevWindow(portList) 
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
