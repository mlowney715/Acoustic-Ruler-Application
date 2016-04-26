#!/usr/bin/python

import wx
import threading
import thread
import os
import platform
import glob
import datetime
import time
import sys
import serial

from wx.lib.pubsub import pub
from data_ar import Adata, NoDeviceError, StoppableThread


class Single_window(wx.Frame):
    """Open a Single-Channel Window."""

    def __init__(self, parent, ID):
        wx.Frame.__init__(self, parent, ID, "Single Channel System",
                size=(700,600), style=wx.MINIMIZE_BOX
                          |wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)
        self.data = Adata('ruler.cfg')
        self.setup()
        
    def setup(self):
        """Create the Single-Channel Window Elements."""
        self.statusbar = self.CreateStatusBar()
        pub.subscribe(self.update_feed,'update_feed')   

        # Setup the menus
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        qmi = wx.MenuItem(fileMenu, 110, '&Quit\tCtrl+Q', "Quit Application")
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.quit_application, qmi)
        editMenu = wx.Menu()
        editPref = editMenu.Append(wx.ID_ANY, '&Preferences...',
                                   "Change speed of sound or data log path")
        self.Bind(wx.EVT_MENU, self.open_preferences, editPref)
        configDevice = editMenu.Append(wx.ID_ANY, '&Configure',
                                       "Configure Measuring Device")
        self.Bind(wx.EVT_MENU, self.open_configuration, configDevice)
        helpMenu = wx.Menu()
        helpMenu.Append(wx.ID_ANY,'&About')
        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(helpMenu, '&Help')

        # Place the menubar and panel for everything below
        self.SetMenuBar(menubar)
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        font_std = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        font_stdBold = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)

        # Create measure section buttons and labels
        measureBtn = wx.Button(panel, size=(110,100),label="Measure")
        measureBtn.SetFont(wx.Font(14,  wx.SWISS, wx.NORMAL, wx.BOLD))
        playBtn = wx.Button(panel, size=(50,50), label="|>")
        playBtn.SetFont(font_std)
        stopBtn = wx.Button(panel, size=(50,50), label="|=|")
        stopBtn.SetFont(font_std)
        str_trgChan = wx.StaticText(panel, -1, "Channel 1 (Speaker 1: Mic 1)")
        str_trgChan.SetFont(font_stdBold)
        distanceLabel = wx.StaticText(panel, -1, "Distance:")
        distanceLabel.SetFont(font_std)
        self.distance_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '', size=(84,22),
                                           style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        self.distance_txtBox.SetFont(font_std)
        self.distance_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        self.metrics = ['cm','m']
        self.imperials = ['in','ft']
        self.distanceUnitCombobox = wx.ComboBox(panel, -1, size=(80,27),
                                                choices=self.metrics,
                                                style=wx.CB_READONLY)
        self.distanceUnitCombobox.SetValue(self.metrics[0])
        self.distanceUnitCombobox.SetFont(font_std)
        self.metricBtn = wx.RadioButton(panel, label="Metric",
                                                 style=wx.RB_GROUP)
        self.metricBtn.SetValue(True)
        self.metricBtn.SetFont(font_std)
        self.imperialBtn = wx.RadioButton(panel, label="Imperial")
        self.imperialBtn.SetFont(font_std)
        propTimeLabel = wx.StaticText(panel, -1, "Propogation Time:") 
        propTimeLabel.SetFont(font_std)
        self.propdelay_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),
                                            style=wx.TE_READONLY
                                            |wx.ALIGN_RIGHT)
        self.propdelay_txtBox.SetFont(font_std)
        self.propdelay_txtBox.SetBackgroundColour(wx.Colour(255,250,250))
        propdelayUnitLabel = wx.StaticText(panel, -1, "msec")
        propdelayUnitLabel.SetFont(font_std)
        gainLabel = wx.StaticText(panel, -1, "Gain:")
        gainLabel.SetFont(font_std)
        gainTextBox = wx.TextCtrl(panel, wx.ID_ANY, '',size=(84,22),
                                  style=wx.TE_READONLY|wx.ALIGN_RIGHT)
        gainTextBox.SetFont(font_std)
        gainTextBox.SetBackgroundColour(wx.Colour(255,250,250))
        gainUnitLabel = wx.StaticText(panel, -1, '%')
        gainUnitLabel.SetFont(font_std)

        # Map the items created above into their places in the section
        trgMeasureGridBag = wx.GridBagSizer(5,8)
        trgMeasureGridBag.Add(str_trgChan, pos=(0, 0), span=(1,8),
                              flag=wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM
                                   |wx.ALIGN_CENTRE, border=5)
        trgMeasureGridBag.Add(measureBtn, pos=(1, 0), span=(4,3),
                              flag=wx.TOP|wx.LEFT|wx.Right|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(playBtn, pos=(5, 0), span=(1,1),
                              flag=wx.TOP|wx.LEFT|wx.Right|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(stopBtn, pos=(5, 1), span=(1,1),
                              flag=wx.TOP|wx.LEFT|wx.Right|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(distanceLabel, pos=(1, 3), 
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.distance_txtBox, pos=(1, 4),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.distanceUnitCombobox, pos=(1, 5),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.metricBtn, pos=(1, 6),
                              flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=5)
        trgMeasureGridBag.Add(self.imperialBtn, pos=(1, 7),
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
        trgMeasureStaticBox = wx.StaticBox(panel, label="")
        trgMeasureStaticBox.SetFont(font_stdBold)
        trgMeasureBoxSizer = wx.StaticBoxSizer(trgMeasureStaticBox,
                                               wx.HORIZONTAL)
        trgMeasureBoxSizer.Add(trgMeasureGridBag,
                               flag=wx.EXPAND|wx.LEFT|wx.TOP
                                    |wx.BOTTOM|wx.RIGHT,
                               border=10)

        # Bind the buttons to their respective functions
        self.metricBtn.Bind(wx.EVT_RADIOBUTTON, self.change_distance_units)
        self.distanceUnitCombobox.Bind(wx.EVT_COMBOBOX,
                                       self.update_distance_text)
        self.imperialBtn.Bind(wx.EVT_RADIOBUTTON, self.change_distance_units)
        measureBtn.Bind(wx.EVT_BUTTON, self.trig_measure)
        
#        playBtn.Bind(wx.EVT_BUTTON, self.trig_repeat)
#        stopBtn.Bind(wx.EVT_BUTTON, self.stop_repeating)
        

        # Create Status Panel Labels
        UnitLabel = wx.StaticText(panel, -1, "Unit ID:")
        UnitLabel.SetFont(font_std)

        statusGridSizer = wx.GridBagSizer(1,1)
        statusGridSizer.Add(UnitLabel, pos=(0,0),
                            flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                            border=5)
        statusStaticBox = wx.StaticBox(panel, label="Status")
        statusStaticBox.SetFont(font_stdBold)
        statusBoxSizer =wx.StaticBoxSizer(statusStaticBox, wx.HORIZONTAL)
        statusBoxSizer.Add(statusGridSizer,
                           flag=wx.EXPAND|wx.LEFT|wx.TOP|wx.BOTTOM|wx.RIGHT,
                           border=25)

        # Create feed textbox
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

        # Map The sections onto the panel
        sizer = wx.GridBagSizer(2,2)
        sizer.Add(trgMeasureBoxSizer, pos=(0,0),span=(1,2),
                  flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        sizer.Add(statusBoxSizer, pos=(1,0), span=(1,2),
                  flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        sizer.Add(feedBoxSizer, pos=(2,0),span=(1,2),
                  flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)
        panel.SetSizerAndFit(sizer)

    def quit_application(self, event):
        """Quit The Application when File->Quit is clicked."""
        self.Close()
        self.data.quit()

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
        """Change the units of measurement and convert the current units when
        the metric or imperial radio buttons are pressed.
        """
        metricState = self.metricBtn.GetValue()
        imperialState = self.imperialBtn.GetValue()

        # if self.distance_txtBox.GetValue() != "":
        last_value = float(self.distance_txtBox.GetValue())

        last_units = self.distanceUnitCombobox.GetValue()

        if imperialState == True:
            self.distanceUnitCombobox.Clear()
            self.distanceUnitCombobox.AppendItems(self.imperials)
            self.distanceUnitCombobox.SetValue(self.imperials[0])
        elif metricState == True:
            self.distanceUnitCombobox.Clear()
            self.distanceUnitCombobox.AppendItems(self.metrics)
            self.distanceUnitCombobox.SetValue(self.metrics[0])

        current_units = self.distanceUnitCombobox.GetValue()

        if self.distance_txtBox.GetValue() != "":
            if (last_units == "cm" 
                    and current_units == "in"):
                self.distance_txtBox.SetValue(str((last_value)/2.54))
            elif (last_units == "m" 
                    and current_units == "in"):
                self.distance_txtBox.SetValue(str((last_value)*100/2.54))
            elif (last_units == "in" 
                    and current_units == "cm"):
                self.distance_txtBox.SetValue(str((last_value)*2.54))
            elif (last_units == "ft"
                    and current_units == "cm"):
                self.distance_txtBox.SetValue(str((last_value)*12*2.54))

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
 
#     def trig_repeat(self, event):
#         try:
#             self.rep_thread = StoppableThread(self.data)
#             self.rep_thread.start()
# 
#         except NoDeviceError:
#             pub.sendMessage('update_feed',
#                             msg="Error Connecting to Device.\n", 
#                             arg2='wx.DEFAULT')
# 
#     def stop_repeating(self, event):
#         self.rep_thread.stop()
#         pub.sendMessage('update_feed',
#                         msg=str(self.rep_thread.count)+" Measurements Taken.\n",
#                         arg2='wx.DEFAULT')
#         self.rep_thread.join()

    def trig_measure(self,event):
        """Trigger a measurement and display the results in the proper
        units.
        """
        try:
            units = self.distanceUnitCombobox.GetValue()
            distance, delay = self.data.measure(units)
            self.distance_txtBox.SetValue(str(distance))
            self.propdelay_txtBox.SetValue(str(delay))

            # Properly format the time of measurement in the live feed:
            pub.sendMessage('update_feed',
                            msg="Measurement Taken at "
                            +str(datetime.datetime.now().time().hour)+":",
                            arg2='wx.DEFAULT')

            if datetime.datetime.now().time().minute < 10:
                pub.sendMessage('update_feed', msg="0", arg2='wx.DEFAULT')

            pub.sendMessage('update_feed',
                            msg=str(datetime.datetime.now().time().minute)+":",
                            arg2='wx.DEFAULT')

            if datetime.datetime.now().time().second < 10:
                pub.sendMessage('update_feed', msg="0", arg2='wx.DEFAULT')

            pub.sendMessage('update_feed',
                             msg=str(datetime.datetime.now().time().second)
                             +'\n', arg2='wx.DEFAULT')
        except NoDeviceError:
            pub.sendMessage('update_feed',
                            msg="Error Connecting to Device.\n", 
                            arg2='wx.DEFAULT')
        

    def update_distance_text(self, last_val):
        """Convert the current units in the distance text-box when new units
        are selected in the combobox.
        """
        last_value = float(self.distance_txtBox.GetValue())
        current_units = self.distanceUnitCombobox.GetValue()
        if current_units == "m":
            self.distance_txtBox.SetValue(str((last_value)/100.00))
        elif current_units == "cm":
            self.distance_txtBox.SetValue(str((last_value)*100.00))
        elif current_units == "ft":
            self.distance_txtBox.SetValue(str((last_value)/12.00))
        elif current_units == "in":
            self.distance_txtBox.SetValue(str((last_value)*12.00))

class Single_pref(wx.Dialog):
    """Open the preferences window for the Single Channel System."""

    def __init__(self,parent,ID):
        wx.Dialog.__init__(self,parent, ID, "Edit Preferences", size=(670,300),
                           style=wx.MINIMIZE_BOX|wx.CAPTION|wx.CLOSE_BOX)
        self.data = Adata('ruler.cfg')
        self.setup()

        
    def setup(self):
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        font_std = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

        str_speedSoundLabel = wx.StaticText(panel, -1, 'Speed of Sound:')
        self.speedSound_txtBox = wx.TextCtrl(panel, wx.ID_ANY, str(self.data.speed),
                                             size=(84,22),
                                             style=wx.ALIGN_RIGHT)
        str_speedLabel = wx.StaticText(panel, -1, 'm/s')
        locLabel = wx.StaticText(panel, -1, 'Data Logger Location:')
        self.path_txtBox = wx.TextCtrl(panel, wx.ID_ANY, self.data.path,
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
            if newspeed != self.data.speed:
                self.data.changespeed(newspeed)
                pub.sendMessage('update_feed',
                                msg="Speed of Sound changed to: "
                                   +str(self.data.speed)+" m/s\n",
                                arg2='wx.DEFAULT')
            if newpath != self.data.path:
                self.data.changepath(newpath)
                pub.sendMessage('update_feed',
                                msg="Log File Path changed to: "
                                   +str(self.data.path)+"\n",
                                arg2='wx.DEFAULT')
        except ValueError:
            pub.sendMessage('update_feed',
                            msg="Error Changing Preferences.\n",
                            arg2='wx.RED')
        self.MakeModal(False)
        self.Close()
        event.Skip()

class Single_deviceconf(wx.Dialog):
    """Open the configuration window for a Single-Channel System."""

    def __init__(self, parent, ID):
        wx.Dialog.__init__(self,parent, ID, "Configure Device",size=(510,350),
                style=wx.MINIMIZE_BOX| wx.CAPTION |wx.CLOSE_BOX)

        self.data = Adata('ruler.cfg')
        self.setup()

    def setup(self):
        """Create The Configuration Window"""
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetAutoLayout(1)
        self.font_std = wx.Font(12,  wx.SWISS, wx.NORMAL, wx.NORMAL)

        serialSys_label = wx.StaticText(panel, -1, "System Available:")
        serialSys_comboBox = wx.ComboBox(panel, -1, size=(200, 30),
                                         choices=list(self.scan_serial(self)),
                                         style=wx.CB_READONLY)
        serialSys_comboBox.SetSelection(0)
        serialSys_refresh_Btn = wx.Button(panel, size=(100,30),
                                          label="Refresh")

        network_label = wx.StaticText(panel, -1, "Choose a Network:")
        self.network_comboBox = wx.ComboBox(panel, -1, size=(200,30),
                                       choices=list(self.scan_wifi(self)),
                                       style=wx.CB_READONLY)
        self.network_comboBox.SetSelection(0)
        network_refresh_Btn = wx.Button(panel, size=(100,30), label="Refresh")
#         network_refresh_Btn.Bind(wx.EVT_BUTTON, self.setup)

        password_label = wx.StaticText(panel, -1, "Password:")
        self.password_txtBox = wx.TextCtrl(panel, wx.ID_ANY, '', size=(200,27),
                                      style=wx.ALIGN_LEFT|wx.TE_PASSWORD)

        pushBtn = wx.Button(panel, size=(100,30), label="Push")
        pushBtn.bind(wx.EVT_BUTTON, self.push_wireless)
        closeBtn = wx.Button(panel, size=(130,30), label="Close")
        closeBtn.Bind(wx.EVT_BUTTON, self.close_configuration)
        calibrateSysBtn = wx.Button(panel, size=(130,30),label="Calibrate")
#         calibrateSysBtn.Bind(wx.EVT_BUTTON, self.calibrate_device)

        serialSys_label.SetFont(self.font_std)
        serialSys_comboBox.SetFont(self.font_std)
        serialSys_refresh_Btn.SetFont(self.font_std)
        network_label.SetFont(self.font_std)
        self.network_comboBox.SetFont(self.font_std)
        network_refresh_Btn.SetFont(self.font_std)
        password_label.SetFont(self.font_std)
        self.password_txtBox.SetFont(self.font_std)
        pushBtn.SetFont(self.font_std)
        closeBtn.SetFont(self.font_std)
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
        wirelessGridSizer.Add(self.network_comboBox, pos=(0,1),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)
        wirelessGridSizer.Add(network_refresh_Btn, pos=(0,2),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)
        wirelessGridSizer.Add(password_label, pos=(1,0),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)
        wirelessGridSizer.Add(self.password_txtBox, pos=(1,1),
                              flag=wx.TOP|wx.ALIGN_LEFT|wx.BOTTOM|wx.LEFT,
                              border=5)
        wirelessGridSizer.Add(pushBtn, pos=(1,2),
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
        btnBoxSizer.Add(calibrateSysBtn, flag=wx.LEFT, border=30)
        btnBoxSizer.Add(closeBtn, flag=wx.RIGHT, border=5)

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

    def close_configuration(self,event):
        """Close the Configuration Window when the close button is clicked."""
        self.Destroy()
        event.Skip()
        
    def scan_serial(self, event):
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
    
    def scan_wifi(self, event):
        """Scan the wireless access points to create a list of potential
        connections
        """
        networks = self.data.get_networks()
        return networks

    def push_wireless(self, event):
        """Push the network SSID and passkey to the device so the device can be
        disconnected from serial.
        """
        ssid = self.network_comboBox.GetValue()
        passkey = self.password_txtBox.GetValue()
        self.data.go_wireless(ssid, passkey)

    def calibrate_device(self, event):
        """Instruct and supervise the device calibration process."""
        message = """Place Microphone as close as possible to speaker.\n
        Click 'OK' to start system calibration."""
        Dlg = wx.MessageDialog(None, message, "Start System Calibration",
                               wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
        Dlg.SetFont(self.font_std)
        if Dlg.ShowModal() == wx.ID_OK:
            bi = wx.BusyInfo("Calibrating System, please wait...", self)
            time.sleep(1)
            bi2 = wx.BusyInfo("Done!", self)
            time.sleep(1)
            bi.Destroy()
            bi2.Destroy()


if __name__ == '__main__':
    app = wx.App(redirect=True)
    Mainframe = Single_window(parent=None,ID=999)
    Mainframe.Centre()
    Mainframe.Show()
    app.MainLoop()
