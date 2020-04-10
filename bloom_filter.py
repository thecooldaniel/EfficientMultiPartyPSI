import hashlib, math

class bloom_filter(object):
  # m = number of 'bits' desired in the filter
  # n = number of elemnts expected to be stored
  # hashToUse = reference to a function to use as a hash
	def __init__(self, m, n, hashToUse):
		self.m = m
		self.hash = hashToUse
		# Calculate the optimal k number of hash functions to minimize collision from the values m and n
		self.k = GetNumHashFuncs(m, n)
		self.indices = [0] * m

	def Add(self, message):
		hi = self.GenerateIndices(message)
		for i in hi:
			self.indices[i] = 1
		print("Indices for value \"" + message + "\"")
		print(hi)
	
	def Check(self, message):
		hi = self.GenerateIndices(message)
		found = True
		for i in hi:
			if( self.indices[i] != 1):
				found = False
				break
		if found:
			print("The value \"" + message + "\" was found")
		else:
			print("The value \"" + message + "\" is not present in the Bloom filter")

	def Print(self):
		print("Current indices for this Bloom filter:")
		print(self.indices)
		
	def GenerateIndices(self, message):
		hi = []
		for _ in range(0, self.k):
			index, message = self.HashFunction(message)
			hi.append(index)
		return hi

	def HashFunction(self, message):
		message = message.encode()
		m = self.hash(message)
		mhex = m.hexdigest()
		mdec = int(mhex, 16)
		return (mdec % self.m, mhex)

def GetNumHashFuncs(m, n):
	return math.ceil( (m/n) * math.log(2) )

def BFtest(m, n, hashToUse ):
	
	BF = bloom_filter(128, 10, hashlib.sha256)

	BF.Add("hello")
	BF.Add("there")
	BF.Add("obi")
	BF.Add("wan")
	BF.Add("kenobi")

	BF.Check("hello")
	BF.Check("there")
	BF.Check("obi")
	BF.Check("wan")
	BF.Check("kenobi")

	# This is not present, but is found
	BF.Check("this should not be found")

	BF.Print()