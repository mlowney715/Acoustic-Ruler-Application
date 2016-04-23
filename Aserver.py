from socket import *
import struct
import serial

class Aserver:

    def __init__(self, serialName):
        try:
            self.ser = serial.Serial(serialName, timeout=1)
        except serial.serialutil.SerialException:
             raise DeviceConnectionError

    def getdelay(self):
        self.ser.write(b'm')
        bin_delay = self.ser.read(16)
        bin_delay = '\0'*(4-len(bin_delay)) + bin_delay
        delay = struct.unpack('f', bin_delay)[0]
        return delay

    def go_wireless(self, serverName, serverPort):
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)

    def get_wireless_delay(self):
        self.clientSocket.settimeout(1)
        try:
            cue = 'm'
            self.clientSocket.sendto(cue,(self.serverName,
                                          self.serverPort))
            delay, serverAddress = self.clientSocket.recvfrom(2048)
            return float(delay)
        except:
            raise DeviceConnectionError

    def closeSocket(self):
        self.clientSocket.close()

    def closeSerial(self):
        self.ser.close()

class DeviceConnectionError(Exception):
    pass
