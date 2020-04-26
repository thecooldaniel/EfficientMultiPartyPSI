import protocol
import helpers
import hashes as h
import bloom_filter as bf
import garbled_bloom_filter as gbf

NumPlayers = 3 
PlayerInputSize = 5
Nbf = 21
SecParam = 20
Nmaxones = 10
bitLength = 128
p = 0.25
a = 0.3

Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, p, a, SecParam, bitLength, Nbf)
Protocol.perform_RandomOT()
Protocol.get_AllPlayersOnes()
Protocol.performCutandChoose()

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
