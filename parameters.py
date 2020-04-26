import math
import helpers

class Paramaters(object):
    def __init__(self, NumPlayers, Nmaxones, PlayerInputSize, SecParam, bitLength, p, a):
        self.NumPlayers = NumPlayers
        self.Nmaxones = Nmaxones
        self.PlayerInputSize = PlayerInputSize
        self.p = p
        self.a = a
        self.b = 0.05
        self.Nbf = self.Calc_Nbf()
        self.SecParam = SecParam
        self.bitLength = bitLength // 8 #uRandom takes bytes, not bits
        self.shared_random = helpers.uRandomInt(16) % 10000
        self.k = math.ceil( (self.Nbf / PlayerInputSize) * math.log(2) )

        # TODO: Add logic that will increment Nmaxones to increase gamme to 0 if negative
        self.p1bound = self.Calc_p1bound()
        self.gamma = self.Calc_Gamma()
        if(not self.CheckGamma(self.gamma, self.p1bound)):
            print("Gamma out of bounds, please reconfigure the input parameters")
            exit()
        self.Not = self.Calc_Not()
        self.gammaStar = self.Calc_GammaStar()
        if(not self.CheckGamma(self.gammaStar, self.Not)):
            print("GammaStar out of bounds, please reconfigure the input parameters")
            exit()
        print("k = {}".format(self.k))
        print("Not = {}".format(self.Not))
        print("gamma = {}".format(self.gamma))
        print("gammaStar = {}".format(self.gammaStar))

    def CheckGamma(self, gamma, bound):
        r = (self.SecParam + math.sqrt( pow(self.SecParam, 2) + ( 8 * self.SecParam * bound ) ) ) / (2 * self.p * bound)
        return gamma <= r

    def Calc_p1bound(self):
        return self.PlayerInputSize * self.k + self.Nmaxones

    def Calc_Gamma(self):
        x = self.p * self.p1bound
        r = math.floor( ( (self.Nmaxones - (x) ) / x ) )
        return int(r)

    def Calc_Not(self):
        r = math.ceil(self.p1bound / self.a)
        return int(r)

    def Calc_GammaStar(self):
        x = self.p  * self.Not
        r = math.floor( (self.Not - (self.Nbf + x)) / ( x ) )
        return int(r)

    def Calc_Nbf(self):
        m = -(self.PlayerInputSize * math.log(self.b))/(math.log(2)**2)
        return int(m)