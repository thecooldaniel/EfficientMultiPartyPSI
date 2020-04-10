import  players
import  commitment_scheme as CM
import  bloom_filter as BF
import  security_params as SP
import  math


# Set parameters
NumPlayers = 3
PlayerInputSize = 3
Nbf = 3
k = BF.GetNumHashFuncs(Nbf, PlayerInputSize)
SecParam = 20
Nmaxones = 1
p = 0.25
a = 0.5

Protocol_Params = SP.Security_Params(Nmaxones, PlayerInputSize, k, p, a, SecParam, Nbf)

players = players.Players(NumPlayers)
# scheme = CM.CommitmentScheme()
# players.broadcast("test")
players.perform_random_ot(Protocol_Params.a, Protocol_Params.Not)
print("Player 0 has " + str( players.players[0].getNumberOfOnes() ) + " ones. Should be: " + str( Protocol_Params.Not * (NumPlayers - 1) ) )
print("Player 1 has " + str( players.players[1].getNumberOfOnes() ) + " ones. Ideal: " + str( Protocol_Params.Not * Protocol_Params.a ))
print("Player 2 has " + str( players.players[2].getNumberOfOnes() ) + " ones. Ideal: " + str( Protocol_Params.Not * Protocol_Params.a ))
print("\'a\' defined as " + str( Protocol_Params.a ));