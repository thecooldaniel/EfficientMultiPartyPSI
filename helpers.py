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

# Convert a utf-8 string to int
def string_to_int(string):
  i = string.encode('utf8')
  i = binascii.hexlify(i)
  i = int(i, 16)
  return i

# Convert an int to utf-8
def int_to_string(num):
  i = hex(num)
  i = i[2:]
  i = i.encode('ascii')
  i = binascii.unhexlify(i)
  i = i.decode('utf-8')
  return i

def xor_byte_array(c, d):
  return bytes([ a ^ b for (a,b) in zip(c, d) ])
