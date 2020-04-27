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

# Initialize the protocol by calculating parameters,
# creating the players, and generating random inputs
# Note: at least 1 shared value is guaranteed
Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a)

# Perform the random oblivious transfer simulation for P0...Pt
Protocol.perform_RandomOT()
Protocol.print_PlayerROTTable()
Protocol.print_PlayerMessageStats()

# Perform cut-and-choose simulation for P0...Pt
Protocol.perform_CutandChoose()

# Create bloom filters for P1...Pt
Protocol.create_BloomFilters()

# Create P1...Pt's injective functions
Protocol.create_InjectiveFunctions()

# Instantiate P0's and P1's rGBF objects
Protocol.create_RandomizedGBFs()

# P0 performs XOR summation on its own j_messages[injective_func] where bit=1
# P1 performs XOR summation on all P1...Pt's j_messages[injective_func] where bit = P1...Pt's choice
Protocol.perform_XORsummation()

# P0 calculates summary values for all elements of its input set
# P1 calculates summary values for all elements of its input set (Every P1...Pt)
Protocol.perform_SummaryValues()

# P1 receives P0s summary values, compares them to its own
# Intersections are recorded and output
Protocol.perform_Output()