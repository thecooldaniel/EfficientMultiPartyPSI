import random_ot as OT
import helpers
import commitment_scheme as CM


class Players(object):

    def __init__(self, numberOfPlayers):
        self.players = [Player] * numberOfPlayers
        self.transfers = [OT.transfer]
        for i in range(0, numberOfPlayers):
            self.players[i] = Player(i)

    def broadcast(self, message):
        print("Broadcasting " + message + " to all players")
        for player in self.players:
            reply = player.send(message)
            print(reply)


class Player(object):
    def __init__(self, id):
        self.id = id
        self.messages = []
        print("Player " + str(self.id) + " created")

    def send(self, message):
        return "Player " + str(self.id) + " ack"

    def chooseOTbit(self, weight):
        r = helpers.uRandomInt(1) % 100
        weighted = 1 if (r / 100 <= weight) else 0
        return weighted

    def receiveOTmessage(self, bits):
        message = OT.message(bits)
        self.messages.append(message)

    def getNumberOfOnes(self):
        total = 0
        for message in self.messages:
            total += message.isOne()
        return total

    def computeAndStoreCommits(self):
        
        for i in range(0, len(self.messages)):
            bit = 1 if  self.messages[i].isOne() else 0
            open = CM.CommitmentScheme.Open(self.messages[i].bits[bit])
            m = []
            m[bit] = open
            m[1-bit] = 0
            self.messages[i].storeOpenValues()
        
