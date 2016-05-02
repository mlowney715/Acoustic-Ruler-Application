# ar_UDPServer.py
# Section 2.7.1 UDP Socket Programming page 161

from socket import *
import os

serverPort = 5678
serverSocket = socket(AF_INET, SOCK_DGRAM)
thisIP = ''

while thisIP is not '':
    f = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    thisIP = f.read()

serverSocket.bind((thisIP, serverPort))
print thisIP

delay = 0.0004
gain = 0.75
ack = '<<ACK>>'
ID = "AR1"
cue = None

while cue != '<<Q>>':
    print "The server is ready to receive at port "+str(serverPort)
    cue, clientAddress = serverSocket.recvfrom(2048)
    if cue == '<<M>>':
        serverSocket.sendto(str(delay)+"||"+str(gain), clientAddress)
        print "The server measured for "+clientAddress[0]
    elif cue == '<<C>>':
        serverSocket.sendto(str(cal_delay)+"||"+str(ID), clientAddress)
        print "The server calibrated for "+clientAddress[0]

os.system("sudo shutdown now")
