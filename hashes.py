import hashlib

class hashes(object):
    def __init__(self, count):
        # self.length = length
        self.count = count
        self.hash = hashlib.sha256

    # This is not secure. Thankfully this isnt production!
    def getHash(self, id, value):
        h = self.hash()
        h.update(str(id).encode())
        h.update(value.encode())
        return h.digest()


def new(count):
    return hashes(count)