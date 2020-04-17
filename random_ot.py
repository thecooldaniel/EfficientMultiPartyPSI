class message(object):

    def __init__(self, bits, transferID):
        self.bits = bits
        self.opens = []
        self.transferID = transferID

    def isOne(self):
        return 1 if self.bits[1] != 0 else 0

    def storeOpenValues(self, opens):
        for i in range(0, len(self.bits)):
            self.opens.append(opens[i])


class transfer(object):
    def __init__(self, index, messages):
        self.messages = messages

