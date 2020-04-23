import message as ms
import bloom_filter
import garbled_bloom_filter as gbf
import helpers

# Base player class. Houses properties and methods common to both player types
class Player(object):
    def __init__(self, id, params):
        self.id = id
        self.messages = []
        self.c_messages = []
        self.j_messages = []
        self.params = params
        print("Player {} created".format(self.id))

    def identify(self):
        return self.id

    def createBloomFilter(self, hashes):
        self.bloom_filter = bloom_filter.new(self.params.Nbf, self.params.PlayerInputSize, hashes)

    # Choose a bit 1, 0 weighted according to self.params.a as provided by protocol
    def pickBit(self):
        r = helpers.uRandomInt(16) % 100
        return 1 if (r / 100 < self.params.a) else 0

    def receiveOTMessage(self, message: ms.message):
        self.messages.append(message)
    
    def getTotalOnes(self):
        total = 0
        for message in self.messages:
            if isinstance(message, list):
                for m in message:
                    total += 1 if m.bit == 1 else 0
            else:
                if message.bit == 1:
                    total += 1
        return total

# Imagine a bicycle wheel. A "spoke" player is one on the outside
# All players P2+ will be spoke players
class PlayerSpoke(Player):
    def storeMessage(self, message):
        self.messages.append(message)

# Imagine a bicycle wheel. A "hub" player is one in the middle
# p0 and p1 will both always be hub players
class PlayerHub(Player):
    def storeTransfer(self, transfer):
        self.messages.append(transfer)
    
    def createGarbledBloomFilter(self, hashes):
        self.garbled_bloom_filter = gbf.new(self.params.Nbf, self.params.PlayerInputSize, self.params.bitLength, hashes)
