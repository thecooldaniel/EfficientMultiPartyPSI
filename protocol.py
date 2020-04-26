import new_parameters as pm
import players
import hashes
import bloom_filter as bf
import random_oblivious_transfer as rot
import math

class protocol(object):
    def __init__(self, NumPlayers, PlayerInputSize, SecParam, bitLength):
        self.players = []
        self.params = pm.parameters(NumPlayers, PlayerInputSize, SecParam, bitLength)
        self.create_Players()
        self.hashes = hashes.new(self.params.k)
        self.create_BloomFilters()
    
    def create_Players(self):
        print("\nSimulating players joining protocol. Total: {}".format(self.params.NumPlayers))
        p0 = players.PlayerHub(0, self.params)
        p1 = players.PlayerHub(1, self.params)
        self.players.append(p0)
        self.players.append(p1)

        for i in range(2, self.params.NumPlayers):
            p = players.PlayerSpoke(i, self.params)
            self.players.append(p)
    
    def create_BloomFilters(self):
        print("\nCreating Bloom Filter simulation. BF length: {}".format(self.params.Nbf))
        for player in self.players:
            player.create_BloomFilter(self.hashes)
            # player.bloom_filter.print("Player {}: ".format(player.id))

    def create_InjectiveFunctions(self):
        print("\nCreating injective function simulation for every Pi:")
        for player in self.players:
            if player.id != 0:
                player.create_InjectiveFunction()

    def test_BloomFilter(self):
        m = "hello"
        print("\nPopulating Bloom Filters with value \"{}\"".format(m))
        for player in self.players:
            player.bloom_filter.add(m)
            player.bloom_filter.print("Player {}: ".format(player.id))
        print("\nEnsuring uniformity...")
        valid = True
        for i in range(0, len(self.players[0].bloom_filter.indices)):
            p0 = self.players[0].bloom_filter.indices[i]
            for j in range(1, len(self.players)):
                if self.players[j].bloom_filter.indices[i] != p0:
                    valid = False
                    break
        if valid:
            print("Result: All Bloom Filters equal")
        if not valid:
            print("Result: Bloom filters inconsistent!")

        print("Resetting Bloom Filters...")
        for player in self.players:
            player.bloom_filter.clear()
    
    def perform_RandomOT(self):
        print("\nSimulating Random OT Stage. Performing {} transfers in total:".format(self.params.Not))
        sender = self.players[0]
        receivers = []
        for i in range(1, len(self.players)):
            receivers.append(self.players[i])

        randomOT = rot.random_ot(sender, receivers)
        randomOT.performTransfers()
        randomOT.getAllTransfersFromPlayers()
        randomOT.printAllTransfers()
    
    def get_AllPlayersOnes(self):
        print("\nCounting each player's \"1s\":")
        for player in self.players:
            ones = player.getTotalOnes()
            ideal = self.params.Not * self.params.a
            print("P{} has {} ones. a * Not: {}".format(player.id, ones, ideal))

    def TestOwnershipTheory(self):
        print("Output should be 1")
        print( self.players[0].messages[5][0].owner.messages[50].owner.id )
        self.players[1].id = 6
        print("Output should be 6")
        print( self.players[0].messages[5][0].owner.messages[50].owner.id )
        self.players[1].id = 1

    def perform_CutandChoose(self):
        C = math.floor(self.params.Not * self.params.p)
        for player in self.players:
            for i in range(0, C-1):
                player.c_messages.append(player.messages[i])
                totalOnes = 0
                if player.id != 0:
                    for m in player.c_messages:
                        totalOnes += 1 if m.bit == 1 else 0
                    if totalOnes > self.params.Nmaxones:
                        print("Protocol aborted: Player {} has {} ones, which is more than {}".format(player.id, totalOnes, player.params.Nmaxones))
            for i in range(C, len(player.messages)):
                player.j_messages.append(player.messages[i])


def new(NumPlayers, PlayerInputSize, SecParam, bitLength):
        return protocol(NumPlayers, PlayerInputSize, SecParam, bitLength)
        
