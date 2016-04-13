from socket import *

class Aserver:

	def __init__(self, serverName, serverPort):
		self.serverName = serverName
		self.serverPort = serverPort
		self.clientSocket = socket(AF_INET, SOCK_DGRAM)

	def getdelay(self):
		cue = 'm'
		self.clientSocket.sendto(cue,(self.serverName, self.serverPort))
		delay, serverAddress = self.clientSocket.recvfrom(2048)	# 2048 buffer size
		return float(delay)

	def closeSocket(self):
		self.clientSocket.close()

