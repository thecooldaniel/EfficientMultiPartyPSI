import math
import helpers

class parameters(object):
    def __init__(self, NumPlayers, PlayerInputSize, SecParam, bitLength):

        self.SecParamOptions = [40]
        self.PlayerInputSizeOptions = [64, 4096, 65536, 1048576]

        self.NumPlayers = NumPlayers
        self.bitLength = bitLength // 8 #uRandom takes bytes, not bits
        self.shared_random = helpers.uRandomInt(16) % 10000
        self.PlayerInputSize = PlayerInputSize

        # if PlayerInputSize in self.PlayerInputSizeOptions:
        #     self.PlayerInputSize = PlayerInputSize
        # else:
        #     print("Input size invalid, defaulting to 64")
        #     self.PlayerInputSize = 64

        if SecParam in self.SecParamOptions:
            self.SecParam = SecParam
        else:
            print("Security parameter invalid. Defaulting to 40")
            self.SecParam = 40

        self.p = input_size_params[PlayerInputSize]['p']
        self.k = input_size_params[PlayerInputSize]['k']
        self.Nbf = input_size_params[PlayerInputSize]['Nbf']
        self.Not = input_size_params[PlayerInputSize]['Not']
        self.Nmaxones = input_size_params[PlayerInputSize]['Nmaxones']
        self.a = input_size_params[PlayerInputSize]['a']

        self.calc_Parameters()

    def calc_Parameters(self):
            pStep = 0.001
            cStep = 0.001
            best = 9999999999999999999999999999.0
            pBest = -1
            cBest = -1
            mh1Best = 0
            thresholdbest = 0
            hBest = 0

            for h in range(80, 99):
                p = 0.001
                minOnes = self.PlayerInputSize  * h

                while p < 0.1:
                    c = 2.4
                    sec = 0
                    mh = -1
                    threshold = -1
                    maxOnes, mh, threshold = compute(p, self.SecParam, minOnes, mh, threshold)

                    while sec < 128 and c < 120:
                        c += cStep
                        cPrime  = (self.PlayerInputSize * h * c) / maxOnes
                        sec = math.log2(math.pow(cPrime, h))
                    
                    total = self.PlayerInputSize * h * c / (1 - p)

                    if total < best and sec >= 128.0:
                        best = total
                        pBest = p
                        cBest = c
                        hBest = h
                        mh1Best = mh
                        thresholdbest = threshold
                    
                    p += pStep
            
            if pBest < 0:
                print("n is too small for kappa bit security")
            else:
                self.Nbf = int(self.PlayerInputSize * hBest * cBest)
                self.totalOnesCount = int(mh1Best)
                self.Not = int(computeMh(self.Nbf, pBest, self.SecParam))
                self.Nmaxones = int(thresholdbest)
                self.p  = pBest
                self.k = int(hBest)




# these values and functions derived from Peter Rindal's libPSI library
# Specifically: https://github.com/osu-crypto/libPSI/blob/master/libPSI/MPSI/Rr16/AknBfMPsiReceiver.cpp

# these parameters are pre-computed for kappa = 40
# Which is the security parameter we will be using
input_size_params = {
    4: {
       'Not': 8295,
       'Nmaxones': 138,
       'p': 0.099,
       'k': 94,
       'Nbf': 7196,
       'a': 0.274
    },
    64: {
       'Not': 99372,
       'Nmaxones': 3182,
       'p': 0.099,
       'k': 94,
       'Nbf': 88627,
       'a': 0.274
    },
    4096: {
       'Not': 1187141,
       'Nmaxones': 22958,
       'p': 0.053,
       'k': 94,
       'Nbf': 1121959,
       'a': 0.344
    },
    65536: {
       'Not': 16992857,
       'Nmaxones': 150181,
       'p': 0.024,
       'k': 91,
       'Nbf': 16579297,
       'a': 0.360
    },
    1048576: {
       'Not': 260252093,
       'totalOnesCount': 95333932,
       'Nmaxones': 962092,
       'p': 0.01,
       'k': 90,
       'Nbf': 257635123,
       'a': 0.366
    }
}

def computeMa(p, tau, kappa):
    ma = (p*kappa + p*tau + math.sqrt(kappa*kappa*p*p + 2 * kappa*p*p*tau)) / (p*p)
    return ma

def computeTau(mh, p, kappa):
    tau = p * mh + (kappa + math.sqrt(kappa * kappa + 8 * kappa * p * mh)) / 2
    return tau

def computeMh(minOnes, p, kappa):
    dem = math.sqrt(kappa) * math.sqrt(kappa + p * p + 2 * kappa * p + kappa - 8 * minOnes * p * p + 8 * minOnes * p) + kappa * p + kappa - 2 * minOnes * p + 2 * minOnes
    num = 2 * (p * p - 2 * p + 1)
    mh = dem / num
    return mh

def computeMaxOnes(ma, p, kappa):
    return (1 - p) *ma + math.sqrt(2 * kappa * (p*ma))

def computeMinOnes(n, h):
    return n * h

def compute(p, kappa, minOnes, mh, tau):
    mh = computeMh(minOnes, p, kappa)
    tau = computeTau(mh, p, kappa)
    ma = computeMa(p, tau, kappa)
    maxOnes = computeMaxOnes(ma, p, kappa)
    return (maxOnes, mh, tau)
