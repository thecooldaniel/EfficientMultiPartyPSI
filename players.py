import random_ot as OT, random as rand, helpers, commitment_scheme as CM

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

    # Performs role of FE-OT (Ideal functionality)
    def perform_random_ot(self, weight, iterations=1):
        for i in range(0, iterations):
            print("Performing random OT " + str(i + 1) + " of " + str(iterations) )
            for j in range(1, len(self.players)):
                m = [helpers.uRandomInt(16)]
                m.append( helpers.uRandomInt(16) )
                self.players[0].receiveOTmessage(m)
                # bit will be either 0, or 1
                bit = self.players[j].chooseOTbit(weight)
                m = m.copy()
                m[1 - bit] = 0
                self.players[j].receiveOTmessage(m)

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
        self.messages.append( message )
    
    def getNumberOfOnes(self):
        total = 0
        for message in self.messages:
            total += message.isOne()
        return total
    
    def computeAndStoreCommits(self):
        for message in self.messages:
            CM.CommitmentScheme.Open()
