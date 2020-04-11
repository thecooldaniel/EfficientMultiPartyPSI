import math


class ProtocolParameters(object):
    def __init__(self, Nmaxones, PlayerInputSize, k, p, a, SecParam, Nbf):
        self.Nmaxones = Nmaxones
        self.PlayerInputSize = PlayerInputSize
        self.k = k
        self.p = p
        self.a = a
        self.SecParam = SecParam
        self.Nbf = Nbf

        self.p1bound = self.Calc_p1bound()
        self.gamma = self.Calc_Gamma()
        if(not self.CheckGamma(self.p1bound)):
            print("Gamma out of bounds, please reconfigure the input parameters")
            exit()
        self.Not = self.Calc_Not()
        self.gammaStar = self.Calc_GammaStar()
        if(not self.CheckGamma(self.Not)):
            print("GammaStar out of bounds, please reconfigure the input parameters")
            exit()

    def CheckGamma(self, bound):
        return self.gamma <= (self.SecParam + math.sqrt( pow(self.SecParam, 2) + ( 8 * self.SecParam * bound ) ) ) / (2 * self.p * bound)

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