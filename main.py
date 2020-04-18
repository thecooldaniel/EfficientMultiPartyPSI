import protocol
import helpers
import hashes as h
import bloom_filter as bf

NumPlayers = 3 
PlayerInputSize = 5
Nbf = 20
SecParam = 20
Nmaxones = 10
bitLength = 128
p = 0.25
a = 0.3

Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, p, a, SecParam, bitLength, Nbf)
Protocol.performRandomOT()
Protocol.getPlayerOnes()

a=1