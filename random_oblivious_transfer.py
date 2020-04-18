import message as ms
import players
import helpers

# Simulates the random OT stage
class random_ot(object):
    def __init__(self, sender: players.PlayerHub, receivers: [players.PlayerSpoke]):
        self.sender = sender
        self.receivers = receivers
        self.params = sender.params
        # Todo

    def genRandomString(self):
        m = [0] * 2
        m[0] = helpers.uRandomInt(self.params.bitLength)
        m[1] = helpers.uRandomInt(self.params.bitLength)
        return m
    
    def performTransfers(self):
        for _ in range(0, self.params.Not):
            t = []
            for receiver in self.receivers:
                r = self.genRandomString()
                m = ms.genMessagesFromBitPair(r)
                b = receiver.pickBit()
                receiver.receiveOTMessage(m[b])
                t.append(m[0])
                t.append(m[1])
            self.sender.storeTransfer(t)

