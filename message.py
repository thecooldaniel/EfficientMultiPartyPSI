
# Represents on message in a transfer.
# Every message has a bit:{1,0} and a value
class message(object):
    def __init__(self, bit=-1, message=-1):
        self.bit = bit
        self.message = message
    
    def update(self, bit, value):
        self.bit = bit
        self.value = value

    def get(self):
        return (self.bit, self.message)

def genMessagesFromBitPair(values):
    if len(values) == 2:
        m = [0] * 2
        m[0] = message(0, values[0])
        m[1] = message(1, values[1])
        return m
    else:
        print("Too many bits passed")

