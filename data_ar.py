import datetime
from wifi import Cell, Scheme
from operator import attrgetter
import threading
import time
import os
import ConfigParser
from server_ar import AServer, DeviceConnectionError

class AData:

    def __init__(self, configname):
        self.config = ConfigParser.RawConfigParser()
        if os.path.isfile(configname):
            pass
        else:
            self.newconfig(configname)
        self.load(configname)

    def newconfig(self, configname):
        """Make a configuration file and set the parameters to default
        values.
        """
        self.config.add_section('phys_env')
        self.config.set('phys_env', 'speed_sound', '343')

        self.config.add_section('data_env')
        self.config.set('data_env', 'log_path', './logs')

        # self.config.add_section('socket_info')
        # self.config.set('socket_info', 'device_address', '127.0.0.1')
        # self.config.set('socket_info', 'device_port', '12000')

        self.config.add_section('serial_info')
        self.config.set('serial_info', 'port_name', '/dev/ttyUSB0')

        with open(configname, 'wb') as configfile:
            self.config.write(configfile)
        configfile.close()
        self.load(configname)

    def load(self, configname):
        """Try to load the already existing configuration file. If it is
        corrupt, make a new one and then load it.
        """
        try:
            self.config.read(configname)
            self.speed = self.config.getfloat('phys_env', 'speed_sound')
            self.path = self.config.get('data_env', 'log_path')
            self.changepath(self.path)
            serialPort = self.config.get('serial_info', 'port_name')
            try:
               self.server = AServer(serialPort)
            except DeviceConnectionError:
                self.server = None
        except ConfigParser.Error:
            print "Warning: Corrupt config file. Resetting to defaults..."
            os.remove(configname)
            self.newconfig(configname)
            self.load(configname)

    def changespeed(self, newspeed):
        """Change the speed of sound and update the configuration file."""
        self.config.set('phys_env','speed_sound',newspeed)
        with open('ruler.cfg', 'wb') as configfile:
            self.config.write(configfile)
        configfile.close()
        self.speed = float(newspeed)

    def changepath(self, newpath):
        """Change the path to the log file and update the configuration file.
        """
        if newpath[0] == '~':
            newpath = os.environ['HOME'] + newpath[1:]
        if not os.path.isdir(newpath):
            try:
                os.makedirs(newpath, 0755)
            except OSError:
                print "Permission Denied: mkdir"
                return
        else:
            try:
                test = open(newpath+'/'+'foo', 'w+')
            except IOError:
                print "Warning: No write permission, but path changed."
            try:
                test.close()
            except UnboundLocalError:
                pass
            try:
                os.remove(newpath+'/'+'foo')
            except OSError:
                pass
        self.config.set('data_env','log_path',newpath)
        with open('ruler.cfg', 'wb') as configfile:
            self.config.write(configfile)
        configfile.close()
        self.path = newpath
	
    def measure(self, units):
        """Tell the device to take a measurement and then calculate the
        distance, write to the log file, and return the distance.
        """
        if self.server is not None:
            delay = self.server.get_delay()
            if units == 'm':
                distance = delay*self.speed
            elif units == 'cm':
                distance = delay*self.speed*100
            elif units == 'in':
                distance = (delay*self.speed)*100/2.54
            else:
                distance = (delay*self.speed)*100/(2.54*12)
            log = open(self.path+"/"+"Aruler_log-"+str(datetime.date.today())
                       +".txt", "a+")
            log.write("\nTime: "+str(datetime.datetime.now().time())+"\n")
            log.write("Delay: "+str(delay)+" msec\n")
            log.write("Distance: "+str(distance)+" "+units+'\n')
            return distance, delay
        else:
            raise NoDeviceError

    def get_networks(self):
        """Return a list of SSIDs to populate the list."""
        ssids = self.server.get_networks()
        return ssids

    def go_wireless(self, ssid, passkey):
        """Setup the server for a wireless connection and connect the client
        application to the network.
        """
        self.server.go_wireless('192.168.1.3', 12000, ssid, passkey)

    def quit(self):
       """Close any sockets or serial ports that have been opened."""
        if self.server is not None:
            self.server.closeSerial()
        
class StoppableThread(threading.Thread):
    """Thread with a stop() condition. 
    http://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python
    """

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data
        self._stop = threading.Event()

    def run(self):
        self.count = 0
        while(not self.stopped()):
            self.data.measure('m')
            self.count = self.count + 1
            time.sleep(1)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

class NoDeviceError(Exception):
    pass
