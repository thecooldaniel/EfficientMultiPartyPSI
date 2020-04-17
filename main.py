import math
import protocol as P
import bloom_filter as BF
import pandas as PD

NumPlayers = 3 
PlayerInputSize = 5
Nbf = 10
k = BF.GetNumHashFuncs(Nbf, PlayerInputSize)
SecParam = 40
Nmaxones = 10
p = 0.25
a = 0.3

# Initialize the protocol with the parameters above
Protocol = P.Protocol(Nmaxones, PlayerInputSize, k, p, a, SecParam, Nbf)
Protocol.Report_ProtocolParams()

# Add the players to the protocol
Protocol.AddPlayers(NumPlayers)

Protocol.Perform_RandomOT(Protocol.Params.a, Protocol.Params.Not)
Protocol.Report_PlayerMessages()

Protocol.Perform_CutAndChoose()