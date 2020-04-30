import message as ms
import players
import helpers
import pandas as pd
import os
import PySimpleGUI as sg

# Turn all debug prints to print in a window
print = sg.Print

# Simulates the random OT stage
class random_ot(object):
    def __init__(self, sender: players.PlayerHub, receivers: [players.PlayerSpoke]):
        self.sender = sender
        self.receivers = receivers
        self.params = sender.params
        self.transfers = None
        # Todo

    def genRandomString(self):
        m = [0] * 2
        m[0] = os.urandom(self.params.byteLength)
        m[1] = os.urandom(self.params.byteLength)
        return m
    
    def performTransfers(self):
        for _ in range(0, self.params.Not):
            t = []
            for receiver in self.receivers:
                r = self.genRandomString()
                m = ms.genMessagesFromBitPair(receiver, r)
                b = receiver.pickBit()
                receiver.receiveOTMessage(m[b])
                t.append(m[0])
                t.append(m[1])
            self.sender.store_Transfer(t)
    
    def getAllTransfersFromPlayers(self):
        transfers = []
        for i in range(0, len(self.sender.messages)):
            t = self.getSingleTransferFromPlayers(i)
            transfers.append(t)
        self.transfers = transfers

    def getSingleTransferFromPlayers(self, index):
        t = []
        for j in range(0, len(self.sender.messages[index])):
            r = self.sender.messages[index][j].get()
            owner = "P{}".format(r[0].id) 
            bit = "Bit: " + str(r[1])
            value = r[2]
            t.append( (owner, bit, value) )
        for player in self.receivers:
            r = player.messages[index].get()
            owner = "P{}".format(r[0].id) 
            bit = "Bit: " + str(r[1])
            value = r[2]
            t.append((owner, bit, value))
        return t

    def printAllTransfers(self):
        columns = []
        numPlayers = len(self.receivers) + 1
        numCols = (3 * numPlayers) - 3
        p0Cols = (numPlayers - 1) * 2
        for i in range(0, numCols):
            if i <= p0Cols - 1:
                columns.append("P0")
            else:
                columns.append("P{}".format((i - p0Cols) + 1))
        table = pd.DataFrame(self.transfers, columns = columns)
        return table


