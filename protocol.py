import player as PL
import commitment_scheme as CM
import protocol_parameters as PM
import helpers
import pandas as PD
import math


class Protocol(object):
    """
    Driver for all protocol methods and data structures:
    Players
    Commitment Scheme
    Random OT Simulation
    Cut-and-choose Simulation
    Bloom Filters
    """

    def __init__(self, Nmaxones, PlayerInputSize, k, p, a, SecParam, Nbf):
        self.players = []
        self.CM = CM.CommitmentScheme()
        self.Params = PM.ProtocolParameters(Nmaxones, PlayerInputSize, k, p, a, SecParam, Nbf)

    def AddPlayers(self, number):
        p0 = PL.Player_Hub()
        self.players.append(p0)
        for i in range(1, number):
            p = PL.Player_Normal(i)
            self.players.append(p)

    def Abort(self, message="None given"):
        exit("Abort. Reason: " + message)

    def Perform_ValidateCommits(self):
        # TODO
        return True

    def Perform_RandomOT(self, weight, iterations=1):
        """Performs role of FE-OT (Ideal functionality)"""
        for player in self.players:
            player.messages = []
        print("Performing " + str(iterations) + " Random Oblivious Transfers...")
        for i in range(0, iterations):
            for j in range(1, len(self.players)):
                m = [helpers.uRandomInt(16)]
                m.append(helpers.uRandomInt(16))
                self.players[0].receiveOTmessage(m, i)
                # bit will be either 0, or 1
                bit = self.players[j].chooseOTbit(weight)
                m = m.copy()
                m[1 - bit] = 0
                self.players[j].receiveOTmessage(m, i)
    
    def Report_PlayerMessages(self):
        """Prints player's messages"""
        columns = []
        rows = []
        headers = []
        indecies = []
        numTransfers = len(self.players[0].messages)
        def truncate(num):
            return (5, True) if num > 5 else (num, False)
        
        threshold, isTrunc = truncate(numTransfers)

        for i in range(0, len(self.players)):
            ones, zeroes = self.players[i].getMessages(threshold)
            headers.append("P" + str(i) + "'s 1s")
            columns.append(ones)
            headers.append("P" + str(i) + "'s 0s")
            columns.append(zeroes)

        for i in range(0, threshold):
            indecies.append(i + 1)

        indecies.append("...")
        indecies.append(numTransfers)
        for i in range(0, threshold + 2):
            tmp = []
            for column in columns:
                tmp.append(column[i])
            rows.append(tmp)
        table = PD.DataFrame(rows, columns = headers, index = indecies)
        print(table)

    def Report_ProtocolParams(self):
        print("Number of Hash Functions: {}".format(self.Params.k))
        print("Number of OTS: {}".format(self.Params.Not))
        print("Number of Max ones: {}".format(self.Params.Nmaxones))
        print("Gamma: {}".format(self.Params.gamma))
        print("GammaStar: {}".format(self.Params.gammaStar))

    def Perform_CutAndChoose(self):
        if not self.Perform_ValidateCommits():
            self.Abort("Failed cut and choose") 
        C = math.ceil( self.Params.Not * self.Params.p )
        print(C)

