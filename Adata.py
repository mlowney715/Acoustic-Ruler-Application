import datetime
import os
import ConfigParser
from Aserver import Aserver, DeviceTimeoutError

class Adata:

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
        self.config.set('data_env', 'log_path', './')

        self.config.add_section('socket_info')
        self.config.set('socket_info', 'device_address', '127.0.0.1')
        self.config.set('socket_info', 'device_port', '12000')

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
            self.server = Aserver(self.config.get('socket_info', 'device_address'),
                                  int(self.config.get('socket_info',
                                                      'device_port')))
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
	
    def measure(self):
        """Tell the device to take a measurement and then calculate the
        distance, write to the log file, and return the distance.
        """
        try:
            delay = self.server.getdelay()
            distance = self.speed*float(delay)
            log = open(self.path+"/"+"SingleChannelLog-"+str(datetime.date.today())
                       +".txt", "a+")
            log.write("\nTime: "+str(datetime.datetime.now().time())+"\n")
            log.write("Delay: " + str(delay)+" msec\n")
            log.write("Distance: " + str(distance)+" m\n\n")
            return distance
        except DeviceTimeoutError:
            raise NoDeviceError

    def quit(self):
        """Close any sockets or serial ports that have been opened."""
        self.server.closeSocket()
        

class NoDeviceError(Exception):
    pass
