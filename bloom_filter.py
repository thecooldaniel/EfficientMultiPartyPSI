import math
import hashes as h
import helpers

class bloom_filter(object):
    def __init__(self, m, n, hashes):
        self.m = m
        self.n = n
        self.hashes = hashes
        self.indices = [0] * m

    def genIndicesForValue(self, value) -> bool:
        indices = []
        for i in range(0, self.hashes.count):
            index = self.hashes.getHash(i, value)
            index = helpers.decfromdigest(index, self.m)
            indices.append(index)
        return indices

    def add(self, value):
        indices = self.genIndicesForValue(value)
        for index in indices:
            self.indices[index] = 1

    def check(self, value):
        present = True
        indices = self.genIndicesForValue(value)
        for index in indices:
            if self.indices[index] != 1:
                present = False
                break
        if present:
            return True
            # print("Value \"{}\" found".format(value))
        else:
            return False
            # print("Value \"{}\" not found".format(value))
    
    def clear(self):
        for i in range(0, len(self.indices)):
            self.indices[i] = 0
    
    def print(self, prefix=""):
        print("{} {}".format(prefix, self.indices))


def new(m, n, hashes):
    return bloom_filter(m, n, hashes)