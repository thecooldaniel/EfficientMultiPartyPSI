import random_ot as OT
import helpers
import commitment_scheme as CM


class Players(object):

    def __init__(self, numberOfPlayers):
        self.players = [Player_Normal] * numberOfPlayers
        self.transfers = [OT.transfer]
        for i in range(0, numberOfPlayers):
            self.players[i] = Player_Normal(i)

    def broadcast(self, message):
        print("Broadcasting " + message + " to all players")
        for player in self.players:
            reply = player.send(message)
            print(reply)


class Player_Normal(object):

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

    def receiveOTmessage(self, bits, transferID):
        message = OT.message(bits, transferID)
        self.messages.append(message)

    def getNumberOfOnes(self):
        total = 0
        for message in self.messages:
            total += message.isOne()
        return total
    
    def getMessages(self, threshold = -1):
        ones = []
        zeroes = []
        for i in range(0, len(self.messages) - 2):
            ones.append(self.messages[i].bits[1])
            zeroes.append(self.messages[i].bits[0])
            if( threshold != -1 and i == threshold - 1):
                ones.append("...")
                zeroes.append("...")
                break
        ones.append(self.messages[len(self.messages) - 1].bits[1])
        zeroes.append(self.messages[len(self.messages) - 1].bits[0])
        return (ones, zeroes)

    def computeAndStoreCommits(self):
        cm = CM.CommitmentScheme()
        for i in range(0, len(self.messages)):
            bit = 1 if self.messages[i].isOne() else 0
            openVal = cm.Open(self.messages[i].bits[bit])
            m = []
            m[bit] = open
            m[1-bit] = 0
            self.messages[i].storeOpenValues()

class Player_Hub(Player_Normal):
    def __init__(self):
        self.id = 0
        self.messages = [[]]
        print("Player 0 created")