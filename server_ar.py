from socket import *
import struct
import serial
from wifi import Cell, Scheme
from operator import attrgetter

class AServer:

    def __init__(self, serialName):
        self.wireless = True
        # try:
        #     self.ser = serial.Serial(serialName, timeout=1)
        # except serial.serialutil.SerialException:
        #      raise DeviceConnectionError

    def get_delay(self):
        """Take a measurement from the device using serial unless a wireless
        scheme is set up.
        """
        # Still need to get gain
        if self.wireless is False:
            self.ser.write(b'<<M>>')
            bin_delay = self.ser.read(16)
            bin_delay = '\0'*(4-len(bin_delay)) + bin_delay
            delay = struct.unpack('f', bin_delay)[0]
        else:
            delay = self.get_wireless_delay()
        return delay

    def get_wireless_delay(self):
        """Cue a measurement using sockets over the wireless connection.
        Returns a floating point number as the measured delay.
        """
        self.serverName = '192.168.2.102'
        self.serverPort = 5678
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(3)
        try:
            cue = '<<M>>'
            self.clientSocket.sendto(cue,(self.serverName,
                                          self.serverPort))
            response, serverAddress = self.clientSocket.recvfrom(2048)
            measurement = response.split('||')
            delay = measurement[0]
            gain = measurement[1]
            return float(delay), float(gain)
        except:
            raise DeviceConnectionError

    def get_ID(self):
        """Send a message to the server to start a calibration."""
        if self.wireless is False:
            self.ser.write(b'<<I>>')
            bin_ID = self.ser.read(16)
            return struct.unpack('s', bin_ID)[0]
        else:
            return self.get_wireless_ID()

    def get_wireless_ID(self):
        """Cue a measurement using sockets over the wireless connection.
        Returns a floating point number as the measured delay.
        """
        self.serverName = '192.168.2.102'
        self.serverPort = 5678
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(3)
        # try:
        cue = '<<I>>'
        self.clientSocket.sendto(cue,(self.serverName,
                                      self.serverPort))
        ID, serverAddress = self.clientSocket.recvfrom(2048)
        return ID
        # except:
        #     raise DeviceConnectionError

    def get_calibration(self):
        """Send a message to the server to start a calibration."""
        if self.wireless is False:
            self.ser.write(b'<<C>>')
            bin_ack = self.ser.read(16)
            return struct.unpack('s', bin_ack)[0]
        else:
            return self.get_wireless_calibration()

    def get_wireless_calibration(self):
        """Use a UDP socket to send a message to start calibration."""
        self.serverName = '192.168.2.102'
        self.serverPort = 5678
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(3)
        try:
            cue = '<<C>>'
            self.clientSocket.sendto(cue,(self.serverName,
                                          self.serverPort))
            response, serverAddress = self.clientSocket.recvfrom(2048)
            calibration = response.split('||')
            cal_delay = calibration[0]
            ID = calibration[1]
            return float(cal_delay), ID
        except:
            raise DeviceConnectionError

    def get_networks(self):
        """Form a list of available Wi-Fi cells, keeping only the best quality
        Cell out of any duplicates. Return a list of SSIDs, sorted by quality.
        """
        unfiltered = Cell.all('wlan0')
        unfiltered_sorted = sorted(unfiltered, key = attrgetter('quality'),
                                   reverse=True)
        seen = set()
        self.networks = []
        ssids = []
        s = attrgetter('ssid')
        for i in unfiltered_sorted:
            if s(i) not in seen:
                self.networks.append(i)
                ssids.append(s(i))
                seen.add(s(i))
        return ssids

    def go_wireless(self, serverName, serverPort, ssid, passkey=None):
        """Switch from a serial connection to a wireless connection and set up
        a UDP socket
        """
        # serverName is the IP address of the Raspberry Pi over the network
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)

        # A scheme is needed to connect to a Wi-Fi access point.
        scheme = Scheme.for_cell('wlan0', 'ruler', ssid, passkey)
        scheme.save()
        scheme.activate()
        self.wireless = True

    def shut_down(self):
        """Close the UDP socket opened to request a measurement over a wireless
        connection.
        """
        self.serverName = '192.168.2.102'
        self.serverPort = 5678
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(3)
        try:
            cue = '<<Q>>'
            self.clientSocket.sendto(cue,(self.serverName,
                                          self.serverPort))
            self.clientSocket.close()
        except:
            pass


    # def close_serial(self):
    #     """Close the serial port that was opened to request a measurement over
    #     a serial connection.
    #     """
    #     self.ser.close()

class DeviceConnectionError(Exception):
    pass
