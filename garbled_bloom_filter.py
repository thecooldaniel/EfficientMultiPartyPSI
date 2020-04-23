import math
import hashes as h
import helpers
import os

class garbled_bloom_filter(object):
    def __init__(self, m, n, bitLength, hashes):
        self.m = m
        self.n = n
        self.bitLength = bitLength
        self.hashes = hashes
        self.indices = [None] * m

    def add(self, val):
        emptyslot = -1
        finalShare = val

        if isinstance(finalShare, str):
            finalShare = helpers.string_to_int(finalShare)

        finalShare = finalShare.to_bytes(self.bitLength, 'big')
        for i in range(0, self.hashes.count):
            j = self.hashes.getHash(i, val)
            j = helpers.decfromdigest(j, self.m)
            if self.indices[j] == None:
                if emptyslot == -1:
                    emptyslot = j
                else:
                    r = os.urandom(self.bitLength)
                    self.indices[j] = r
                    finalShare = bytes([ a ^ b for (a,b) in zip(finalShare, r) ])
            else:
                finalShare = bytes([ a ^ b for (a,b) in zip(finalShare, self.indices[j]) ])
        self.indices[emptyslot] = finalShare

    def check(self, val):
        recovered = int(0).to_bytes(self.bitLength, 'big')
        for i in range(0, self.hashes.count):
            j = self.hashes.getHash(i, val)
            j = helpers.decfromdigest(j, self.m)
            recovered = bytes([ a ^ b for (a,b) in zip(recovered, self.indices[j]) ])
        return int.from_bytes(recovered, 'big')
        
    def clear(self):
        for i in range(0, len(self.indices)):
            self.indices[i] = 0

    def print(self, prefix=""):
        print("{} {}".format(prefix, self.indices))

# Pattern to gain the "new" keyword
# in the namespace without naming the main
# class "new"
def new(m, n, bitLength, hashes):
    return garbled_bloom_filter(m, n, bitLength, hashes)