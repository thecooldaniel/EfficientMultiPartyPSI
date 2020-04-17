import binascii

def hexfromdigest(digest):
    return binascii.hexlify(digest)

def decfromdigest(digest, domain=-1):
    hexs = hexfromdigest(digest)
    dec = int(hexs, 16)
    return (dec % domain) if (domain > 0) else dec
