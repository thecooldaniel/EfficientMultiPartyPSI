import binascii
import os
import pandas as pd

# Helper functions for annoying processes

# Get a hex string from a byte object
def hexfromdigest(digest):
    return binascii.hexlify(digest)

# Get an int from a byte object
def decfromdigest(digest, domain=-1):
    hexs = hexfromdigest(digest)
    dec = int(hexs, 16)
    return (dec % domain) if (domain > 0) else dec

# Get securely generated random string
def uRandomInt(bytes):
    r = os.urandom(bytes)
    rhex = binascii.hexlify(r)
    return int(rhex, 16)

def buildTotalTransfers(players):
    transfers = []
    for i in range(0, len(players[0].messages)):
        t = []
        for player in players:
            if player.id == 0:
                for j in range(0, len(player.messages[i])):
                    r = player.messages[i][j].get()
                    t.append(r)
            else:
                r = player.messages[i].get()
                t.append(r)
        transfers.append(t)
    return transfers

def printTransfers(transfers, numPlayers):
    columns = []
    indices = []
    numCols = (3 * numPlayers) - 3
    p0Cols = (numPlayers - 1) * 2
    for i in range(0, numCols):
        if i <= p0Cols - 1:
            columns.append("P0")
        else:
            columns.append("P{}".format((i - p0Cols) + 1))
    table = pd.DataFrame(transfers, columns = columns)
    print(table)
