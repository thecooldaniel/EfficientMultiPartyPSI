import hashlib

# Houses and generates the k has functions used for the bloom filters
class hashes(object):
    def __init__(self, count):
        # self.length = length
        self.count = count
        self.hash = hashlib.sha256
    
    # When given an id, always seeds the hash with that id
    # This is not secure. Don't do this at home kids.
    def getHash(self, id, value):
        h = self.hash()
        h.update(str(id).encode())
        h.update(value.encode())
        return h.digest()

# Pattern to gain the "new" keyword
# in the namespace without naming the main
# class "new"
def new(count):
    return hashes(count)