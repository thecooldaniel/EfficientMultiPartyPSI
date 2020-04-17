import parameters as pm
import players
import hashes
import bloom_filter as bf

class init(object):
    def __init__(self, NumPlayers, Nmaxones, PlayerInputSize, p, a, SecParam, Nbf):
        self.players = []
        self.params = pm.Paramaters(NumPlayers, Nmaxones, PlayerInputSize, p, a, SecParam, Nbf)
        self.initPlayers()
        self.hashes = hashes.new(self.params.k)
        self.initBloomFilters()

    def initPlayers(self):
        print("Initializing Players...")
        p0 = players.PlayerHub(0)
        p1 = players.PlayerHub(1)
        self.players.append(p0)
        self.players.append(p1)

        for i in range(2, self.params.NumPlayers):
            p = players.PlayerSpoke(i)
            self.players.append(p)
    
    def initBloomFilters(self):
        print("\nInitializing Bloom Filters...")
        m = self.params.Nbf
        n = self.params.PlayerInputSize
        hashes = self.hashes
        for player in self.players:
            player.createBloomFilter(m, n, hashes)
            player.bloom_filter.print("Player {}: ".format(player.id))

    def testBloomFilters(self):
        m = "hello"
        for player in self.players:
            player.bloom_filter.add(m)
            player.bloom_filter.print("Player {}'s bloom filter: ".format(player.id))
