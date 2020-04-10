import hashlib, math, players

class CommitmentScheme(object):
    def __init__(self, parameter = "iamalittleteapot"):
        self.parameter = parameter
        self.hash = hashlib.sha256
    
    def Commit(self, players, playerid):
        players.broadcast(playerid, "commit")

    def Open(self, message):
        h = self.hash( self.parameter + str(message))
        return h.hexdigest()