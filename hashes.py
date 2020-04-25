import hashlib
import helpers

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
        if isinstance(value, int):
            value = str(value)
        # id = helpers.int_to_string(id)
        h.update(str(id).encode())
        h.update(value.encode())
        return h.digest()
    
    def randomOracle(self, value):
        h = self.hash()
        if isinstance(value, int):
            value = str(value)
        h.update(value.encode())
        return h.digest()

# Pattern to gain the "new" keyword
# in the namespace without naming the main
# class "new"
def new(count):
    return hashes(count)