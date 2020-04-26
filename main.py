import protocol
import helpers
import hashes as h
import bloom_filter as bf
import garbled_bloom_filter as gbf

NumPlayers = 3 
PlayerInputSize = 100
SecParam = 40
Nmaxones = 100
bitLength = 256
p = 0.25 # Fraction of messages to use for Cut and Choose
a = 0.25 # Probability a 1 is chosen by a player
b = 0.05 # Desired probability of a bloom-filter false-positive

Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a, b)
Protocol.perform_RandomOT()
Protocol.get_AllPlayersOnes()
Protocol.perform_CutandChoose()

Protocol.create_InjectiveFunctions()

Protocol.players[0].create_RandomizedGBF(Protocol.hashes)
Protocol.players[0].create_XOR_sums([ Protocol.players[1], Protocol.players[2] ])
vals0 = Protocol.players[0].create_SummaryValsToShare( Protocol.hashes )

Protocol.players[1].create_RandomizedGBF(Protocol.hashes)
Protocol.players[1].create_XOR_sums([ Protocol.players[1], Protocol.players[2] ])
vals1 = Protocol.players[1].create_SummaryValsToShare( Protocol.hashes )

for i in range(0, len(vals0)):
    for j in range(0, len(vals1)):
        if vals0[i] == vals1[j]:
            print("Intersection at {}".format(vals0[i]))


a=1
