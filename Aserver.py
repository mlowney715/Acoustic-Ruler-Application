from socket import *
import struct
import serial

class Aserver:

    def __init__(self, serverName, serverPort):
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)

    def getdelay(self):
        self.clientSocket.settimeout(1)
        try:
            cue = 'm'
            self.clientSocket.sendto(cue,(self.serverName, self.serverPort))
            delay, serverAddress = self.clientSocket.recvfrom(2048)	# 2048 buffer size
            return float(delay)
        except:
            raise DeviceConnectionError

    def closeSocket(self):
        self.clientSocket.close()


class Aserial:

    def __init__(self, portName):
        try:
            self.ser = serial.Serial(portName, timeout=1)
        except serial.serialutil.SerialException:
            raise DeviceConnectionError

    def getdelay(self):
        try:
            self.ser.write(b'm')
            bin_delay = self.ser.read(16)
            delay = struct.unpack('f', bin_delay)[0]
            return delay
        except struct.error:
            raise DeviceConnectionError


class DeviceConnectionError(Exception):
    pass
