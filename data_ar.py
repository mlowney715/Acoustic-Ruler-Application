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
        self.configname = configname
        self.config = ConfigParser.RawConfigParser()
        if os.path.isfile(configname):
            pass
        else:
            self.new_config(configname)
        self.load_config(configname)

    def new_config(self, configname):
        """Make a configuration file and set the parameters to default
        values.
        """
        self.config.add_section('phys_env')
        self.config.set('phys_env', 'speed_sound', '343')

        self.config.add_section('data_env')
        self.config.set('data_env', 'log_path', './logs')

        with open(configname, 'wb') as configfile:
            self.config.write(configfile)
        configfile.close()
        self.load_config(configname)

    def load_config(self, configname):
        """Try to load the already existing configuration file. If it is
        corrupt, make a new one and then load it.
        """
        try:
            self.config.read(configname)
            self.set_path(self.get_path())
            try:
                self.server = AServer('/dev/ttyUSB0')
            except DeviceConnectionError:
                self.server = None
        except ConfigParser.Error:
            print "Warning: Corrupt config file. Resetting to defaults..."
            os.remove(configname)
            self.new_config(configname)
            self.load_config(configname)

    def get_speed(self):
        self.config.read(self.configname)
        return self.config.getfloat('phys_env', 'speed_sound')

    def set_speed(self, newspeed):
        """Change the speed of sound and update the configuration file."""
        self.config.set('phys_env','speed_sound',newspeed)
        with open('ruler.cfg', 'wb') as configfile:
            self.config.write(configfile)
        configfile.close()

    def get_path(self):
        self.config.read(self.configname)
        return self.config.get('data_env', 'log_path')

    def set_path(self, newpath):
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
	
    def get_ID(self):
        """Obtain Identification from the Device. Acoustic Rulers get treated
        just like any other young adult when purchasing alcohol.
        """
        if self.server is not None:
            try:
                ID = self.server.get_ID()
                return ID
            except DeviceConnectionError:
                raise NoDeviceError
        else:
            raise NoDeviceError

    def measure(self, units):
        """Tell the device to take a measurement and then calculate the
        distance, write to the log file, and return the distance.
        """
        if self.server is not None:
            try:
                delay, gain = self.server.get_delay()
                if units == 'm':
                    distance = delay*self.get_speed()
                elif units == 'cm':
                    distance = delay*self.get_speed()*100
                elif units == 'in':
                    distance = (delay*self.get_speed())*100/2.54
                else:
                    distance = (delay*self.get_speed())*100/(2.54*12)
                log = open(self.get_path()+"/"+"Aruler_log-"+str(datetime.date.today())
                           +".txt", "a+")
                log.write("\nTime: "+str(datetime.datetime.now().time())+'\n')
                log.write("Delay: "+str(delay)+" msec\n")
                log.write("Distance: "+str(distance)+" "+units+'\n')
                log.write("Gain at input: "+str(gain*100)+"%\n")
                log.close()
                return distance, delay, gain
            except DeviceConnectionError:
                raise NoDeviceError
        else:
            raise NoDeviceError

    def calibrate(self):
        """Begin Calibration process."""
        if self.server is not None:
            try:
                ack = self.server.get_calibration()
                if ack == '<<ACK>>':
                    return True
                else:
                    return False
            except DeviceConnectionError:
                raise NoDeviceError
        else:
            raise NoDeviceError

    def format_time(self):
        """Format time as (h)h:mm:ss"""
        formatted_time = []
        formatted_time.append(str(datetime.datetime.now().time().hour)+":")

        if datetime.datetime.now().time().minute < 10:
            formatted_time.append("0")

        formatted_time.append(str(datetime.datetime.now().time().minute)+":")

        if datetime.datetime.now().time().second < 10:
            formatted_time.append("0")

        formatted_time.append(str(datetime.datetime.now().time().second))

        return ''.join(formatted_time)

    def scan(self):
        """Return a list of SSIDs to populate the list."""
        ssids = self.server.get_networks()
        return ssids

    # def go_wireless(self, ssid, passkey):
    #     """Setup the server for a wireless connection and connect the client
    #     application to the network.
    #     """
    #     self.server.go_wireless('acousticpi.local', 5678, ssid, passkey)

    def quit(self):
        """Close any sockets or serial ports that have been opened."""
        if self.server is None:
            pass
        else:
            self.server.close_serial()
        
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
