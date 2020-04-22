import math
import hashes as h
import helpers

class garbled_bloom_filter(object):
    def __init__(self, m, n, hashes):
        self.m = m
        self.n = n 
        self.hashes = hashes
        self.indices = [None] * m

    # Given an input, generates an index of domain Nbf 
    # for all k
    def genIndicesForValue(self, value) -> bool:
        indices = []
        for i in range(0, self.hashes.count):
            index = self.hashes.getHash(i, value)
            index = helpers.decfromdigest(index, self.m)
            indices.append(index)
        return indices

    def add

    def clear(self):
        for i in range(0, len(self.indices)):
            self.indices[i] = 0

    def print(self, prefix=""):
        print("{} {}".format(prefix, self.indices))

# Pattern to gain the "new" keyword
# in the namespace without naming the main
# class "new"
def new(m, n, hashes):
    return garbled_bloom_filter(m, n, hashes)