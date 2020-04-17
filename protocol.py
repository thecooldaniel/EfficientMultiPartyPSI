import parameters as pm
import players
import hashes

class init(object):
    def __init__(self, NumPlayers, Nmaxones, PlayerInputSize, p, a, SecParam, Nbf):
        self.players = []
        self.params = pm.Paramaters(NumPlayers, Nmaxones, PlayerInputSize, p, a, SecParam, Nbf)
        self.createPlayers()
        self.hashes = hashes.new(self.params.k)

    def createPlayers(self):
        p0 = players.PlayerHub(0)
        p1 = players.PlayerHub(1)
        self.players.append(p0)
        self.players.append(p1)

        for i in range(2, self.params.NumPlayers):
            p = players.PlayerSpoke(i)
            self.players.append(p)

