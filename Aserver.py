from socket import *

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
            raise DeviceTimeoutError

    def closeSocket(self):
        self.clientSocket.close()

class DeviceTimeoutError(Exception):
    pass
