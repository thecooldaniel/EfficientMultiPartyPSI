import math
import hashes as h
import helpers
import PySimpleGUI as sg

# Turn all debug prints to print in a window
print = sg.Print

# Houses the data structures and methods for creating and maintaining a Bloom Filter
class bloom_filter(object):
    def __init__(self, m, n, hashes):
        self.m = m
        self.n = n
        self.hashes = hashes
        self.indices = [0] * m

    # Given an input, generates an index of domain Nbf 
    # for all k
    def genIndicesForValue(self, value) -> bool:
        indices = []
        for i in range(0, self.hashes.count):
            index = self.hashes.getHash(i, value)
            index = helpers.decfromdigest(index, self.m)
            indices.append(index)
        return indices

    # Stores a value in the filter
    def add(self, value):
        indices = self.genIndicesForValue(value)
        for index in indices:
            self.indices[index] = 1

    # Check if a value exists
    # Will never give a false negative. 
    # Might give a false positive
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

# Pattern to gain the "new" keyword
# in the namespace without naming the main
# class "new"
def new(m, n, hashes):
    return bloom_filter(m, n, hashes)