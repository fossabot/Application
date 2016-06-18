# -*- coding: utf-8 -*-


import socket
import sys

HOST = 'localhost'	# Symbolic name, meaning all available interfaces
PORT = 5555	# Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
    s2.bind((HOST, PORT+1))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' - ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    conn.send("ack")
    conn2, addr2 = s2.accept()
    print 'Connected with ' + addr2[0] + ':' + str(addr2[1])
    conn2.send("ack")