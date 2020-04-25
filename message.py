# Represents on message in a transfer.
# Every message has a bit:{1,0} and a value
class message(object):
    def __init__(self, owner, bit=-1, message=-1):
        self.owner = owner
        self.bit = bit
        self.message = message
    
    def update(self, bit, value):
        self.bit = bit
        self.value = value

    def get(self):
        return (self.owner, self.bit, self.message)

def genMessagesFromBitPair(owner, values):
    if len(values) == 2:
        m = [0] * 2
        m[0] = message(owner, 0, values[0])
        m[1] = message(owner, 1, values[1])
        return m
    else:
        print("Too many bits passed")

