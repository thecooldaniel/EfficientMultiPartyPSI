class message(object):
    def __init__(self, bits):
        self.bits = bits
        self.opens = []
    def isOne(self):
        return 1 if self.bits[1] != 0 else 0

class transfer(object):
    def __init__(self, index, messages):
        self.messages = messages

        