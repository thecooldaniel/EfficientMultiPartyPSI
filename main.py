import protocol
import helpers
import hashes as h
import bloom_filter as bf
import garbled_bloom_filter as gbf

NumPlayers = 3 
PlayerInputSize = 20 # 10
SecParam = 40
bitLength = 128

# These parameters are meant for illustration and fast execution
# they are not considered secure or optimal
Nmaxones = 80 # 40
p = 0.3 # 0.25 # Fraction of messages to use for Cut and Choose
a = 0.27 # 0.25 # Probability a 1 is chosen by a player
disableChecks = False

# Initialize the protocol by calculating parameters,
# creating the players, and generating random inputs
# Note: at least 1 shared value is guaranteed
Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a, disableChecks)
print("\nStarting protocol...")
print("k = {}".format(Protocol.params.k))
print("Not = {}".format(Protocol.params.Not))
print("gamma = {}".format(Protocol.params.gamma))
print("gammaStar = {} \n".format(Protocol.params.gammaStar))
print("\nSimulating players joining protocol. Total: {}".format(Protocol.params.NumPlayers))
print("\nStep finished\n")

# Perform the random oblivious transfer simulation for P0...Pt
print("\nPerforming Random Oblivious Transfer simulation. {} transfers in total:".format(Protocol.params.Not))
Protocol.perform_RandomOT()
print(Protocol.print_PlayerROTTable())
print("\nCounting each player's \"1s\":")
print(Protocol.print_PlayerMessageStats())
print("\nStep finished\n")


# Perform cut-and-choose simulation for P0...Pt
print("Performing Cut and Choose simulation. Size of c: {}. Size of j: {}".format(Protocol.params.C, Protocol.params.Not - Protocol.params.C))
Protocol.perform_CutandChoose()
print("\nStep finished\n")

# Create bloom filters for P1...Pt
print("Creating Bloom Filters. BF length: {}".format(Protocol.params.Nbf))
Protocol.create_BloomFilters()
print("\nStep finished\n")

# Create P1...Pt's injective functions
print("Creating injective functions for every Pi:")
print(Protocol.create_InjectiveFunctions())
print("\nStep finished\n")

print("\nCreating randomized GBF for every Pi")
# Instantiate P0's and P1's rGBF objects
Protocol.create_RandomizedGBFs()
print("\nStep finished\n")

print("\nCalculating final output")
# P0 performs XOR summation on its own j_messages[injective_func] where bit=1
# P1 performs XOR summation on all P1...Pt's j_messages[injective_func] where bit = P1...Pt's choice
Protocol.perform_XORsummation()

# P0 calculates summary values for all elements of its input set
# P1 calculates summary values for all elements of its input set (Every P1...Pt input values)
Protocol.perform_SummaryValues()

# P1 receives P0s summary values, compares them to its own
# Intersections are recorded and output
print(Protocol.perform_Output())
print("\nStep finished\n")