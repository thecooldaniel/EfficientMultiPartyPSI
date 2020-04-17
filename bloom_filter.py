import math
import hashes as h
import helpers

class new(object):
    def __init__(self, m, n, hashes):
        self.m = m
        self.n = n
        self.hashes = hashes
        self.indices = [0] * m

    def genIndicesForValue(self, value):
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
            print("Value \"{}\" found".format(value))
        else:
            print("Value \"{}\" not found".format(value))
    
    def print(self, prefix=""):
        print("{} {}".format(prefix, self.indices))

