import message

class Player(object):
    def __init__(self, id):
        self.id = id
        self.messages = []
        print("Player {} created".format(self.id))
    
    def identify(self):
        return self.id

class PlayerSpoke(Player):
    def storeMessage(self, message):
        self.messages.append(message)


class PlayerHub(Player):
    def storeTransfer(self, messages):
        self.messages.append(messages)
