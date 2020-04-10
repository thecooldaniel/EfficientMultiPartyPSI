import os, binascii

def uRandomInt(bytes):
    r = os.urandom(bytes)
    rhex = binascii.hexlify(r)
    return int(rhex, 16)
