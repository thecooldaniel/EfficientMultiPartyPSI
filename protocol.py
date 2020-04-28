import parameters as pm
import players
import hashes
import bloom_filter as bf
import random_oblivious_transfer as rot
import math
import PySimpleGUI as sg

# Turn all debug prints to print in a window
print = sg.Print

class protocol(object):
    def __init__(self, NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a):
        self.players = []
        self.params = pm.Paramaters(NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a)
        self.create_Players()
        self.hashes = hashes.new(self.params.k)
        self.sumVals = []
    
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
        print("\nCreating Bloom Filters. BF length: {}".format(self.params.Nbf))
        for player in self.players:
            player.create_BloomFilter(self.hashes)
            # player.bloom_filter.print("Player {}: ".format(player.id))

    def perform_RandomOT(self):
        print("\nPerforming Random Oblivious Transfer simulation. {} transfers in total:".format(self.params.Not))
        sender = self.players[0]
        receivers = []
        for i in range(1, len(self.players)):
            receivers.append(self.players[i])

        self.randomOT = rot.random_ot(sender, receivers)
        self.randomOT.performTransfers()

    def perform_CutandChoose(self):
        C = math.floor(self.params.Not * self.params.p)
        print("\nPerforming Cut and Choose simulation. Size of c: {}. Size of j: {}".format(C, self.params.Not - C))
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

    def create_InjectiveFunctions(self):
        print("\nCreating injective functions for every Pi:")
        for player in self.players:
            if player.id != 0:
                player.create_InjectiveFunction()
    
    def create_RandomizedGBFs(self):
        print("\nCreating randomized GBF for every Pi")
        for player in self.players[:2]:
            player.create_RandomizedGBF(self.hashes)

    def perform_XORsummation(self):
        Pi = self.players[1:]
        for player in self.players[:2]:
            player.create_XOR_sums(Pi)

    def perform_SummaryValues(self):
        self.sumVals = []
        for player in self.players[:2]:
            self.sumVals.append(player.create_SummaryValsToShare(self.hashes))

    def perform_Output(self):
        output = self.players[1].find_Intersections(self.sumVals[0])
        print("\n")
        for player in self.players:
            print("Player {}'s input set: {}".format(player.id, player.inputSet))
        print("\n")
        for index, _ in enumerate(self.sumVals):
            pstr ="["
            for elem in self.sumVals[index]:
                elemm = int.from_bytes(elem, 'big')
                pstr += "{:7.7}..., ".format(str(elemm))
            pstr += "]"
            print("Player {}'s summary values: {}".format(index, pstr))
        
        print("\nIntersections found at these values: {}".format(output))

    def print_PlayerROTTable(self):
        self.randomOT.getAllTransfersFromPlayers()
        self.randomOT.printAllTransfers()
    
    def print_PlayerMessageStats(self):
        print("\nCounting each player's \"1s\":")
        for player in self.players:
            ones = player.getTotalOnes()
            ideal = self.params.Not * self.params.a
            print("P{} has {} ones. a * Not: {}".format(player.id, ones, ideal))


def new(NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a):
        return protocol(NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a)
        