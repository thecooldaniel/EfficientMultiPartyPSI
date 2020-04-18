import protocol
import helpers
import hashes as h
import bloom_filter as bf

NumPlayers = 3 
PlayerInputSize = 5
Nbf = 10
SecParam = 40
Nmaxones = 10
bitLength = 128
p = 0.25
a = 0.3

Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, p, a, SecParam, bitLength, Nbf)
Protocol.performRandomOT()
transfers = helpers.buildTotalTransfers(Protocol.players)
helpers.printTransfers(transfers, Protocol.params.NumPlayers)
a=1