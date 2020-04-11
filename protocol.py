import player as PL
import commitment_scheme as CM
import protocol_parameters as PM
import helpers


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
        for i in range(0, number):
            p = PL.Player(i)
            self.players.append(p)

    def Perform_RandomOT(self, weight, iterations=1):
        """Performs role of FE-OT (Ideal functionality)"""

        print("Performing " + str(iterations) + " Random Oblivious Transfers...")
        for _ in range(0, iterations):
            for j in range(1, len(self.players)):
                m = [helpers.uRandomInt(16)]
                m.append(helpers.uRandomInt(16))
                self.players[0].receiveOTmessage(m)
                # bit will be either 0, or 1
                bit = self.players[j].chooseOTbit(weight)
                m = m.copy()
                m[1 - bit] = 0
                self.players[j].receiveOTmessage(m)