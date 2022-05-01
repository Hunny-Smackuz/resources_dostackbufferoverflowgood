#!/usr/bin/env python2
import socket

# configure the IP and port we're connecting to
RHOST = "<target-ip-here>"
RPORT = 31337

# create a TCP connection (socket)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# Make a message followed by a newline
buf = ""
buf += "Python Script"
buf += "\n"

# send a message down the socket
s.send(buf)

# print out what we sent
print("Sent: {0}".format(buf))

# receive some data from the socket
data = s.recv(1024)

# print out what was received
print("Received: {0}".format(data))
