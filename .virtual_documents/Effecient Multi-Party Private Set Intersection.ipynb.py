get_ipython().run_line_magic("load_ext", " autoreload")
get_ipython().run_line_magic("autoreload", " 2")


import math
import protocol as P
import bloom_filter as BF


NumPlayers = 3 
PlayerInputSize = 5
Nbf = 10
k = BF.GetNumHashFuncs(Nbf, PlayerInputSize)
SecParam = 20
Nmaxones = 10
p = 0.25
a = 0.3

# Initialize the protocol with the parameters above
Protocol = P.Protocol(Nmaxones, PlayerInputSize, k, p, a, SecParam, Nbf)

# Add the players to the protocol
Protocol.AddPlayers(NumPlayers)


Protocol.Perform_RandomOT(Protocol.Params.a, Protocol.Params.Not)
print("Player 0 has " + str(Protocol.players[0].getNumberOfOnes()) + " ones. Should be: " + str(Protocol.Params.Not * (NumPlayers - 1)))
print("Player 1 has " + str(Protocol.players[1].getNumberOfOnes()) + " ones. Ideal: " + str(Protocol.Params.Not * Protocol.Params.a))
print("Player 2 has " + str(Protocol.players[2].getNumberOfOnes()) + " ones. Ideal: " + str(Protocol.Params.Not * Protocol.Params.a))
print("\'a\' defined as " + str(Protocol.Params.a));



