import binascii
import os
import pandas as pd

# Helper functions for annoying processes

# Get a hex string from a byte object
def hexfromdigest(digest):
    return binascii.hexlify(digest)

# Get an int from a byte object
def decfromdigest(digest, domain=-1):
    hexs = hexfromdigest(digest)
    dec = int(hexs, 16)
    return (dec % domain) if (domain > 0) else dec

# Get securely generated random string
def uRandomInt(bytes):
    r = os.urandom(bytes)
    rhex = binascii.hexlify(r)
    return int(rhex, 16)

