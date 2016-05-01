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
        self.serverName = 'acousticpi.local'
        self.serverPort = 5678
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(3)
        try:
            cue = '<<M>>'
            self.clientSocket.sendto(cue,(self.serverName,
                                          self.serverPort))
            delay, serverAddress = self.clientSocket.recvfrom(2048)
            return float(delay)
        except:
            raise DeviceConnectionError

    def identify(self):
        """Send a message to the server to start a calibration."""
        if self.wireless is False:
            self.ser.write(b'<<I>>')
            bin_ack = self.ser.read(16)
            return struct.unpack('s', bin_ID)[0]
        else:
            return self.identify_wireless()

    def identify_wireless(self):
        """Cue a measurement using sockets over the wireless connection.
        Returns a floating point number as the measured delay.
        """
        self.serverName = 'acousticpi.local'
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

    def calibrate(self):
        """Send a message to the server to start a calibration."""
        if self.wireless is False:
            self.ser.write(b'<<C>>')
            bin_ack = self.ser.read(16)
            return struct.unpack('s', bin_ack)[0]
        else:
            return self.calibrate_wireless()

    def calibrate_wireless(self):
        """Cue a measurement using sockets over the wireless connection.
        Returns a floating point number as the measured delay.
        """
        self.serverName = 'acousticpi.local'
        self.serverPort = 5678
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.clientSocket.settimeout(3)
        # try:
        cue = '<<C>>'
        self.clientSocket.sendto(cue,(self.serverName,
                                      self.serverPort))
        ack, serverAddress = self.clientSocket.recvfrom(2048)
        return ack
        # except:
        #     raise DeviceConnectionError

    def scan(self):
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

    def go_wireless(self, serverName, serverPort, ssid, passkey):
        """Switch from a serial connection to a wireless connection and set up
        a UDP socket
        """
        # serverName is the IP address of the Raspberry Pi over the network
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)

        # A scheme is needed to connect to a Wi-Fi access point.
        # scheme = Scheme.for_cell('wlan0', 'ruler', ssid, passkey)
        # scheme.save()
        # scheme.activate()
        # self.wireless = True

    def closeSocket(self):
        """Close the UDP socket opened to request a measurement over a wireless
        connection.
        """
        self.clientSocket.close()

    def closeSerial(self):
        """Close the serial port that was opened to request a measurement over
        a serial connection.
        """
        self.ser.close()

class DeviceConnectionError(Exception):
    pass
