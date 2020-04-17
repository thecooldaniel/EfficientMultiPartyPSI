
class message(object):
    def __init__(self, bit=-1, message=-1):
        self.bit = bit
        self.message = message
    
    def update(self, bit, value):
        self.bit = bit
        self.value = value

    def get(self):
        return (self.bit, self.value)

class transfer(object):
    def __init__(self, messages):
        self.messages = messages

    def append(self, messages):
        self.messages.append(messages)
