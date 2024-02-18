#!/usr/bin/python3
import sys

def ror_str(byte, count):
    binb = bin(byte)[2:].zfill(32)
    binb = binb[-count % 32:] + binb[:-count % 32]
    return int(binb, 2)

esi = sys.argv[1]
edx = 0x0

ror_count = 0

for eax in esi:
    edx = edx + ord(eax)
    if ror_count < len(esi) - 1:
        edx = ror_str(edx, 0xd)
        ror_count += 1

print(hex(edx))
