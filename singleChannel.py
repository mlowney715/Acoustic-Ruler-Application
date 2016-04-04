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

data = Adata('ruler.cfg')

server = Aserver('10.0.0.3', 12000)

class Single_window(wx.Frame):
    """Open a Single-Channel Window."""

    def __init__(self, parent, ID):
        wx.Frame.__init__(self, parent, ID, "Single Channel System",
                          size=(680,650), style=wx.MINIMIZE_BOX
                          |wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)
        self.setup()
        
    def setup(self):
        """Create the Single-Channel Window Elements."""
        self.statusbar = self.CreateStatusBar()
        pub.subscribe(self.update_feed,'update_feed')   

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        returnMain = fileMenu.Append(wx.ID_ANY, '&Main Menu',
                                     "Return to Application Main Menu")
        self.Bind(wx.EVT_MENU, self.return_main_menu, returnMain)
        qmi = wx.MenuItem(fileMenu, 110, '&Quit\tCtrl+Q', "Quit Application")
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.quit_application, qmi)
        editMenu = wx.Menu()
        optionsMenu = wx.Menu()
        optionsMenu.Append(wx.ID_ANY,'&Configure Wi-Fi')
        optionsMenu.Append(wx.ID_ANY,'&Calibrate System')
        helpMenu = wx.Menu()
        helpMenu.Append(wx.ID_ANY,'&About')
        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(optionsMenu, '&Options')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        font_std = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_stdBold = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)

        measureBtn = wx.Button(panel, size=(100,100),label="Measure")
        str_trgChan = wx.StaticText(panel, -1, "Channel 1 (Speaker 1: Mic 1)")
        distanceLabel = wx.StaticText(panel, -1, "Distance:")
        self.distance_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '', size=(84,22),
                                           style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.metrics = ['cm','m']
        self.imperials = ['in','ft']
        self.distanceUnitCombobox = wx.ComboBox(panel, -1, size=(80,27),
                                                choices=self.metrics,
                                                style=wx.CB_READONLY)
        self.distanceUnitCombobox.SetValue(self.metrics[0])
        self.metricUnitRadioBtn = wx.RadioButton(panel, label="Metric",
                                                 style=wx.RB_GROUP)
        self.metricUnitRadioBtn.SetValue(True)
        self.imperialUnitRadioBtn = wx.RadioButton(panel, label="Imperial")
        propTimeLabel = wx.StaticText(panel, -1, "Propogation Time:") 
        self.propdelay_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),
                                            style=wx.TE_READONLY
                                            |wx.ALIGN_RIGHT)
        propdelayUnitLabel = wx.StaticText(panel, -1, "msec")
        gainLabel = wx.StaticText(panel, -1, "Gain:")
        gainTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),
                                  style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        gainUnitLabel = wx.StaticText(panel, -1, '%')
        measureBtn.SetFont(wx.Font(14,  wx.SWISS, wx.NORMAL, wx.BOLD))
        str_trgChan.SetFont(font_stdBold)
        distanceLabel.SetFont(font_std)
        self.distance_txtBox.SetFont(font_std)
        self.distanceUnitCombobox.SetFont(font_std)
        self.metricUnitRadioBtn.SetFont(font_std)
        self.imperialUnitRadioBtn.SetFont(font_std)
        propTimeLabel.SetFont(font_std)
        self.propdelay_txtBox.SetFont(font_std)
        propdelayUnitLabel.SetFont(font_std)
        gainLabel.SetFont(font_std)
        gainTextBox.SetFont(font_std)
        gainUnitLabel.SetFont(font_std)
        self.distance_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        self.propdelay_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        gainTextBox.SetBackgroundColour(wx.Colour(255,250,250))

        trgMeasureGridBag = wx.GridBagSizer(4,8)
        trgMeasureGridBag.Add(str_trgChan, pos=(0, 0), span=(1,8),
                              flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM
                                   |wx.ALIGN_CENTRE, border=5)
        trgMeasureGridBag.Add(measureBtn, pos=(1, 0), span=(4,3),
                              flag=wx.TOP|wx.LEFT|wx.Right|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(distanceLabel, pos=(1, 3), 
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.distance_txtBox, pos=(1, 4),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.distanceUnitCombobox, pos=(1, 5),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.metricUnitRadioBtn, pos=(1, 6),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.imperialUnitRadioBtn, pos=(1, 7),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.Right, border=5)
        trgMeasureGridBag.Add(propTimeLabel, pos=(2, 3),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.propdelay_txtBox, pos=(2, 4),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(propdelayUnitLabel, pos=(2, 5),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainLabel, pos=(3, 3),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainTextBox, pos=(3, 4),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(gainUnitLabel, pos=(3, 5),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureStaticBox = wx.StaticBox(panel, label= "Trigger Measurement")
        trgMeasureStaticBox.SetFont(font_stdBold)
        trgMeasureBoxSizer = wx.StaticBoxSizer(trgMeasureStaticBox,
                                               wx.HORIZONTAL)
        trgMeasureBoxSizer.Add(trgMeasureGridBag,
                               flag=wx.EXPAND|wx.LEFT|wx.TOP
                                    |wx.BOTTOM|wx.RIGHT,
                               border=10)
        self.metricUnitRadioBtn.Bind(wx.EVT_RADIOBUTTON,
                                     self.change_distance_units)
        self.imperialUnitRadioBtn.Bind(wx.EVT_RADIOBUTTON,
                                       self.change_distance_units)
        measureBtn.Bind(wx.EVT_BUTTON, self.trig_measure)

        systemID = wx.StaticText(panel, -1, 'System ID:')
        sysID_field = wx.StaticText(panel, -1, '--------------------')
        wiFiStatus = wx.StaticText(panel, -1, 'Status:')
        wiFiStatus_field = wx.StaticText(panel, -1, '--------------------')
        wiFiSSID = wx.StaticText(panel, -1, 'Wi-Fi SSID:')
        wiFiSSID_field = wx.StaticText(panel, -1, '--------------------')
        systemID.SetFont(font_stdBold)
        sysID_field.SetFont(font_std)
        wiFiStatus.SetFont(font_stdBold)
        wiFiStatus_field.SetFont(font_std)
        wiFiSSID.SetFont(font_stdBold)
        wiFiSSID_field.SetFont(font_std)
        sysStatusGridSizer = wx.GridBagSizer(3,3)
        sysStatusGridSizer.Add(systemID, pos=(0, 0),
                               flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                               border=5)
        sysStatusGridSizer.Add(sysID_field, pos=(0, 2),
                               flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM, border=5)
        sysStatusGridSizer.Add(wiFiStatus, pos=(1,0),
                               flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                               border=5)
        sysStatusGridSizer.Add(wiFiStatus_field, pos=(1,2),
                               flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.RIGHT,
                               border=5)
        sysStatusGridSizer.Add(wiFiSSID, pos=(2,0),
                               flag=wx.LEFT|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM,
                               border=5)
        sysStatusGridSizer.Add(wiFiSSID_field, pos=(2,2),
                               flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.RIGHT,
                               border=5)
        sysStatusStaticBox = wx.StaticBox(panel, label="System Status")
        sysStatusStaticBox.SetFont(font_stdBold)
        sysStatusBoxSizer = wx.StaticBoxSizer(sysStatusStaticBox, wx.HORIZONTAL)
        sysStatusBoxSizer.Add(sysStatusGridSizer,
                              flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT,
                              border=25) 

        editPrefBtn = wx.Button(panel, size=(160,27),
                                label="Edit Preferences")
        configDeviceBtn = wx.Button(panel, size=(160,27),
                                    label="Configure Device")
        searchDeviceBtn = wx.Button(panel, size=(160,27),
                                    label="Search for Device")
        editPrefBtn.SetFont(font_std)
        configDeviceBtn.SetFont(font_std)
        searchDeviceBtn.SetFont(font_std)
        congfiStaticBox = wx.StaticBox(panel, label='')
        congfiStaticBox.SetFont(font_stdBold)
        configBoxSizer = wx.StaticBoxSizer(congfiStaticBox, wx.VERTICAL)
        configBoxSizer.Add(editPrefBtn, flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT,
                           border=20)
        configBoxSizer.Add(configDeviceBtn,
                           flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT,
                           border=20)
        configBoxSizer.Add(searchDeviceBtn,
                           flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,
                           border=20)
        editPrefBtn.Bind(wx.EVT_BUTTON, self.open_preferences)
        configDeviceBtn.Bind(wx.EVT_BUTTON, self.open_configuration)
        searchDeviceBtn.Bind(wx.EVT_BUTTON, self.search_device)

        self.feed_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(500,120),
                       style=wx.TE_READONLY|wx.ALIGN_LEFT|wx.TE_MULTILINE
                            |wx.TE_RICH2)
        self.feed_txtBox.SetFont(font_std)
        self.feed_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        feedStaticBox = wx.StaticBox(panel, label='')
        feedStaticBox.SetFont(font_stdBold)
        feedBoxSizer = wx.StaticBoxSizer(feedStaticBox, wx.VERTICAL)
        feedBoxSizer.Add(self.feed_txtBox,
                         flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.RIGHT, border=1)
        sizer = wx.GridBagSizer(3,2)
        sizer.Add(trgMeasureBoxSizer, pos=(0,0),span=(1,2),
                  flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        sizer.Add(sysStatusBoxSizer, pos=(1,0),
                  flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        sizer.Add(configBoxSizer, pos=(1,1),
                  flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        sizer.Add(feedBoxSizer, pos=(2,0),span=(1,2),
                  flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        panel.SetSizerAndFit(sizer)

    def quit_application(self, event):
        """Quit The Application when File->Quit is clicked."""
        self.Close()
        server.closeSocket()

    def update_feed(self,msg,arg2=None):
        """Update the live feed at the bottom of the window when something
        happens.
        """
        self.feed_txtBox.AppendText(msg)
        if arg2:
            self.feed_txtBox.SetDefaultStyle(wx.TextAttr(arg2))
            
    def return_main_menu(self, event):
        """Return to the splash screen when File->Return to Main is clicked."""
        self.Destroy()
        
    def change_distance_units(self, event):
        """Change the units of measurement and convert the current units."""
        metricState = self.metricUnitRadioBtn.GetValue()
        imperialState = self.imperialUnitRadioBtn.GetValue()

        if self.distance_txtBox.GetValue() != "":
            last_value = float(self.distance_txtBox.GetValue())

        last_unitComboboxValue = self.distanceUnitCombobox.GetValue()

        if imperialState == True:
            self.distanceUnitCombobox.Clear()
            self.distanceUnitCombobox.AppendItems(self.imperials)
            self.distanceUnitCombobox.SetValue(self.imperials[0])
        elif metricState == True:
            self.distanceUnitCombobox.Clear()
            self.distanceUnitCombobox.AppendItems(self.metrics)
            self.distanceUnitCombobox.SetValue(self.metrics[0])

        current_unitComboboxValue = self.distanceUnitCombobox.GetValue()

        if self.distance_txtBox.GetValue() != "":
            if (last_unitComboboxValue == "cm" 
                    and current_unitComboboxValue == "in"):
                self.distance_txtBox.SetValue(str((last_value)/2.54))
            elif (last_unitComboboxValue == "cm" 
                    and current_unitComboboxValue == "ft"):
                self.distance_txtBox.SetValue(str((last_value)* 0.032808))
            elif (last_unitComboboxValue == "m" 
                    and current_unitComboboxValue == "in"):
                self.distance_txtBox.SetValue(str((last_value)* 39.370))
            elif (last_unitComboboxValue == "m" 
                    and current_unitComboboxValue == "ft"):
                self.distance_txtBox.SetValue(str((last_value)/0.3048))
            elif (last_unitComboboxValue == "in" 
                    and current_unitComboboxValue == "cm"):
                self.distance_txtBox.SetValue(str((last_value)*2.54))
            elif (last_unitComboboxValue == "in"
                    and current_unitComboboxValue == "m"):
                self.distance_txtBox.SetValue(str((last_value)/39.370))
            elif (last_unitComboboxValue == "ft"
                    and current_unitComboboxValue == "cm"):
                self.distance_txtBox.SetValue(str((last_value)/0.032808))
            elif (last_unitComboboxValue == "ft"
                    and current_unitComboboxValue == "m"):
                self.distance_txtBox.SetValue(str((last_value)/3.2808))

    def open_preferences(self, event):
        """Open the Preferences Window when the Open Preference button is
        clicked.
        """
        editPrefFrame = Single_pref(parent=self, ID=997)
        editPrefFrame.Centre()
        editPrefFrame.Show()
        editPrefFrame.ShowModal()
        editPrefFrame.Destroy()
        
    def open_configuration(self,event):
        """Open the Device Configuration Window when the Configure Device
        button is clicked.
        """
        configDevFrame = Single_deviceconf(parent=self, ID=996)
        configDevFrame.Centre()
        configDevFrame.Show()
        configDevFrame.ShowModal()
        configDevFrame.Destroy()
 
    def search_device(self,event):
        """Search for a device when the Search For Device button is clicked."""
        bi = wx.BusyInfo("Searching for Device, please wait...", self)
        # **add code here to establish connection with the device over wifi
        time.sleep(3)
        bi2 = wx.BusyInfo("Device found!", self)
        bi.Destroy()
        bi2.Destroy()

    def trig_measure(self,event):
        """Trigger a measurement and display the results in the proper
        units.
        """
        unitComboboxValue = self.distanceUnitCombobox.GetValue()
        delay = server.getdelay()
        distance = data.measure(delay)
        if unitComboboxValue == "m":
            self.distance_txtBox.SetValue('{:0.2f}'.format(distance))
        elif unitComboboxValue == "cm":
            self.distance_txtBox.SetValue('{:0.2f}'.format((distance)*100))
        elif unitComboboxValue == "in":
            self.distance_txtBox.SetValue('{:0.2f}'.format((distance)*39.370))
        elif unitComboboxValue == "ft":
            self.distance_txtBox.SetValue('{:0.2f}'.format((distance)/0.3048))
        self.distance_txtBox.SetValue(str(distance))
        self.propdelay_txtBox.SetValue(str(delay*1000.0))
        '''
        try: 
        delay = server.getdelay()
        data.measure(delay)
        if unitComboboxValue == "m":
            self.distance_txtBox.SetValue(str(delay*data.speed))
        elif unitComboboxValue == "cm":
            self.distance_txtBox.SetValue(str((delay*data.speed)*100))
        elif unitComboboxValue == "in":
            self.distance_txtBox.SetValue(str((delay*data.speed)*39.370))
        elif unitComboboxValue == "ft":
            self.distance_txtBox.SetValue(str((delay*data.speed)/0.3048))

        self.distance_txtBox.SetValue(str(delay*data.speed))
        self.propdelay_txtBox.SetValue(str(delay*1000.0))
        except ServerError:
        print "Error connecting to device"
        '''
        
    def update_distance_text(self,last_val):
        """Do basically the same thing as the change_units function."""
        last_value = self.distance_txtBox.GetValue()
        last_unitComboboxValue = last_val
        current_unitComboboxValue = self.distanceUnitCombobox.GetValue()
        if (last_unitComboboxValue == "cm" 
                and current_unitComboboxValue == "m"):
            self.distance_txtBox.SetValue(str((last_value)/100.0))
        elif (last_unitComboboxValue == "m" 
                and current_unitComboboxValue == "cm"):
            self.distance_txtBox.SetValue(str((last_value)*100.0))
        elif (last_unitComboboxValue == "in" 
                and current_unitComboboxValue == "ft"):
            self.distance_txtBox.SetValue(str((last_value)*0.083333))
        elif (last_unitComboboxValue == "ft" 
                and current_unitComboboxValue == "in"):
            self.distance_txtBox.SetValue(str((last_value)*12.000))


class Single_deviceconf(wx.Dialog):
    """Open the configuration window for a Single-Channel System."""

    def __init__(self, parent, ID):
        wx.Dialog.__init__(self,parent, ID, "Configure Device",size=(510,350),
                style=wx.MINIMIZE_BOX| wx.CAPTION |wx.CLOSE_BOX)

        ports = list(self.scan_serial(self))
        ports.insert(0, "Select Board to connect")
        # # Pass this as an arg. to configDevWindow func. below
        # # Scan ang get wifi networks in the surround area
        # networkList = list(self.network_ports(self))
        # networkList.insert(0,'Select an Access Point')
        self.setup(ports)

    def setup(self, myPorts):
        """Create The Configuration Window"""
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        self.font_std = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.NORMAL)

        serialSys_label = wx.StaticText(panel, -1, "System Available:")
        serialSys_comboBox = wx.ComboBox(panel, -1, size=(200, 30),
                                         choices=myPorts, style=wx.CB_READONLY)
        serialSys_comboBox.SetSelection(0)
        serialSys_refresh_Btn = wx.Button(panel, size=(100,30),
                                          label="Refresh")

        network_label = wx.StaticText(panel, -1, "Choose a Network:")
        network_comboBox = wx.ComboBox(panel,-1, size=(200,30), choices='',
                                       style=wx.CB_READONLY)
        network_comboBox.SetSelection(0)
        network_refresh_Btn = wx.Button(panel, size=(100,30), label="Refresh")

        password_label = wx.StaticText(panel, -1, "Password:")
        password_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '', size=(200,27),
                                      style=wx.ALIGN_LEFT|wx.TE_PASSWORD)

        pushBtn = wx.Button(panel, size=(130,30), label="Push")
        pingBtn = wx.Button(panel, size=(130,30), label="Ping")
        calibrateSysBtn = wx.Button(panel, size=(130,30),label="Calibrate")

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

        serialCommStaticBox = wx.StaticBox(panel,label="Serial")
        serialCommStaticBox.SetFont(self.font_std)
        serialCommBoxSizer = wx.StaticBoxSizer(serialCommStaticBox,
                                               wx.HORIZONTAL)
        serialCommBoxSizer.Add(serialSys_label,
                               flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT,
                               border=5)
        serialCommBoxSizer.Add(serialSys_comboBox,
                               flag=wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT,
                               border=5)
        serialCommBoxSizer.Add(serialSys_refresh_Btn,
                               flag=wx.TOP|wx.BOTTOM|wx.RIGHT|wx.ALIGN_RIGHT,
                               border=5)

        wirelessGridSizer = wx.GridBagSizer(2,3)
        wirelessGridSizer.Add(network_label, pos=(0,0),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)
        wirelessGridSizer.Add(network_comboBox, pos=(0,1),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)
        wirelessGridSizer.Add(network_refresh_Btn, pos=(0,2),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)
        wirelessGridSizer.Add(password_label, pos=(1,0),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)
        wirelessGridSizer.Add(password_txtBox, pos=(1,1),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)

        wirelessGroupBox = wx.StaticBox(panel, label = "Wireless")
        wirelessGroupBox.SetFont(self.font_std)
        wirelessBoxsizer = wx.StaticBoxSizer(wirelessGroupBox, wx.HORIZONTAL)
        wirelessBoxsizer.Add(wirelessGridSizer, flag=wx.TOP|wx.LEFT|wx.BOTTOM,
                             border=10)

        btnStaticBox = wx.StaticBox(panel, label="")
        btnStaticBox.SetFont(self.font_std)
        btnBoxSizer = wx.StaticBoxSizer(btnStaticBox, wx.HORIZONTAL)
        btnBoxSizer.Add(pushBtn, flag=wx.LEFT, border=30)
        btnBoxSizer.Add(pingBtn, flag=wx.LEFT|wx.RIGHT, border=10)
        btnBoxSizer.Add(calibrateSysBtn, flag=wx.RIGHT, border=5)

        configDevGridSizer = wx.GridBagSizer(3,5)
        configDevGridSizer.Add(serialCommBoxSizer, pos=(0,0), span=(0,4),
                               flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM
                                   |wx.LEFT, border=10)
        configDevGridSizer.Add(wirelessBoxsizer, pos=(1,0), span=(1,4),
                               flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM
                                   |wx.LEFT, border=10)
        configDevGridSizer.Add(btnBoxSizer, pos=(2,0), span=(2,4),
                               flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM
                                   |wx.LEFT, border=10)
        panel.SetSizerAndFit(configDevGridSizer)

        self.Bind(wx.EVT_CLOSE,self.close_configuration)
        calibrateSysBtn.Bind(wx.EVT_BUTTON, self.calibrate_device)

    def close_configuration(self,event):
        """Close the Configuration Window when the close button is clicked."""
        self.Destroy()
        event.Skip()
        
    def scan_serial(self,event):
        """Scan the system for serial ports."""
        if str(platform.system()) == 'Windows':
            tempList = ['COM%s' % (i + 1) for i in range(256)]
        elif str(platform.system()) == 'Linux':
            tempList = glob.glob('/dev/tty[A-Za-z]*')
        elif str(platform.system()) == 'Darwin':
            tempList = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError("Unsupported platform")

        results = []
        for a_port in tempList:
            try:
                s = serial.Serial(a_port)
                s.close()
                results.append(a_port)
            except serial.SerialException:
                pass
        return results
    
    def calibrate_device(self,event):
        """Instruct and supervise the device calibration process."""
        message = """Place Microphone as close as possible to speaker.\n
        Click 'OK' to start system calibration."""
        Dlg = wx.MessageDialog(None, message, "Start System Calibration",
                               wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
        Dlg.SetFont(self.font_std)
        if Dlg.ShowModal() == wx.ID_OK:
            bi = wx.BusyInfo("Calibrating System, please wait...", self)
            time.sleep(5)
            bi2 = wx.BusyInfo("Done!", self)
            time.sleep(2)
            bi.Destroy()
            bi2.Destroy()
        Dlg.Destroy()

class Single_pref(wx.Dialog):
    """Open the preferences window for the Single Channel System."""

    def __init__(self,parent,ID):
        wx.Dialog.__init__(self,parent, ID, "Edit Preferences", size=(670,300),
                           style=wx.MINIMIZE_BOX|wx.CAPTION|wx.CLOSE_BOX)
        self.setup()
        
    def setup(self):
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        font_std = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

        str_speedSoundLabel = wx.StaticText(panel, -1, 'Speed of Sound:')
        self.speedSound_txtBox = wx.TextCtrl(panel, wx.ID_ANY, str(data.speed),
                                             size=(84,22),
                                             style=wx.ALIGN_RIGHT)
        str_speedLabel = wx.StaticText(panel, -1, 'm/s')
        locLabel = wx.StaticText(panel, -1, 'Data Logger Location:')
        self.path_txtBox = wx.TextCtrl(panel, wx.ID_ANY, data.path,
                                       size=(500,22),
                                       style=wx.TE_READONLY|wx.ALIGN_LEFT)
        browseBtn = wx.Button(panel, size=(100,27), label="Browse")
        applyBtn = wx.Button(panel,wx.ID_APPLY, size=(100,27))
        cancelBtn = wx.Button(panel,wx.ID_CANCEL, size=(100,27))

        str_speedSoundLabel.SetFont(font_std)
        str_speedLabel.SetFont(font_std)
        self.speedSound_txtBox.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL,
                                               wx.NORMAL))
        self.speedSound_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        self.path_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        locLabel.SetFont(font_std)
        self.path_txtBox.SetFont(font_std)
        browseBtn.SetFont(font_std)
        applyBtn.SetFont(font_std)
        cancelBtn.SetFont(font_std)

        groupBox_speed = wx.StaticBox(panel, label="Edit Speed of Sound")
        groupBox_speed.SetFont(font_std)
        boxsizer_speed = wx.StaticBoxSizer(groupBox_speed, wx.HORIZONTAL)
        boxsizer_speed.Add(str_speedSoundLabel, flag=wx.TOP|wx.LEFT|wx.BOTTOM,
                           border=10)
        boxsizer_speed.Add(self.speedSound_txtBox, flag=wx.LEFT|wx.TOP,
                           border=10)
        boxsizer_speed.Add(str_speedLabel, flag=wx.TOP|wx.LEFT|wx.ALIGN_LEFT,
                           border=10)

        dataLogGridSizer = wx.GridBagSizer(2,2)
        dataLogGridSizer.Add(locLabel, pos=(0,0),
                             flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                             border=5)
        dataLogGridSizer.Add(self.path_txtBox, pos=(1,0),
                             flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                             border=5)
        dataLogGridSizer.Add(browseBtn, pos=(1,1),
                             flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                             border=5)

        groupBox_dataLog = wx.StaticBox(panel, label= 'Data Logger')
        groupBox_dataLog.SetFont(font_std)
        boxsizer_dataLog = wx.StaticBoxSizer(groupBox_dataLog, wx.HORIZONTAL)
        boxsizer_dataLog.Add(dataLogGridSizer, flag=wx.TOP|wx.LEFT|wx.BOTTOM,
                             border=10)

        editPrefGridSizer = wx.GridBagSizer(3,5)
        editPrefGridSizer.Add(boxsizer_speed, pos=(0,0),span=(0,4),
                              flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM
                                  |wx.LEFT, border=5)
        editPrefGridSizer.Add(boxsizer_dataLog, pos=(1,0), span=(1,4),
                              flag=wx.EXPAND|wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM
                                  |wx.LEFT, border=5)
        editPrefGridSizer.Add(applyBtn, pos=(2,2), 
                              flag=wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.LEFT,
                              border=5)
        editPrefGridSizer.Add(cancelBtn, pos=(2,3),
                              flag=wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM|wx.LEFT,
                              border=5)
        panel.SetSizerAndFit(editPrefGridSizer)

        self.Bind(wx.EVT_CLOSE,self.close_preferences)
        cancelBtn.Bind(wx.EVT_BUTTON, self.close_preferences)
        applyBtn.Bind(wx.EVT_BUTTON, self.apply_changes)
        browseBtn.Bind(wx.EVT_BUTTON, self.browse_directories)
        
    def close_preferences(self,event):
        """Close the Preferences Window when the Close button is clicked"""
        self.Destroy()
        event.Skip()
        
    def browse_directories(self,event):
        """Open a directory browser window"""
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            self.path_txtBox.SetValue(str(dlg.GetPath()))
        dlg.Destroy()
        
    def apply_changes(self,event):
        """Change the Configuration File when preferences have been changed."""
        newspeed = float(self.speedSound_txtBox.GetValue())
        newpath = self.path_txtBox.GetValue()
        try:
            if newspeed != data.speed:
                data.changespeed(newspeed)
                pub.sendMessage('update_feed',
                                msg="Speed of Sound changed to: "
                                   +str(data.speed)+"m/s\n",
                                arg2='wx.DEFAULT')
            if newpath != data.path:
                data.changepath(newpath)
                pub.sendMessage('update_feed',
                                msg="Log File Path changed to: "
                                   +str(data.path)+"\n",
                                arg2='wx.DEFAULT')
        except ValueError:
            pub.sendMessage('update_feed',
                            msg="Error Changing Preferences.\n",
                            arg2='wx.RED')
        self.MakeModal(False)
        self.Close()
        event.Skip()
