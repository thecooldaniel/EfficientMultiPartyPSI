import message
import bloom_filter

class Player(object):
    def __init__(self, id):
        self.id = id
        self.messages = []
        print("Player {} created".format(self.id))

    def identify(self):
        return self.id

    def createBloomFilter(self, m, n, hashes):
        self.bloom_filter = bloom_filter.new(m, n, hashes)

class PlayerSpoke(Player):
    def storeMessage(self, message):
        self.messages.append(message)

class PlayerHub(Player):
    def storeTransfer(self, messages):
        self.messages.append(messages)
