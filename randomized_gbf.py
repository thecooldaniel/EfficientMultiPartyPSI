import helpers

class randomized_gbf(object):
    def __init__(self, owner, hashes):
        self.owner = owner
        self.hashes = hashes
        self.indices = []
        self.m = owner.params.Nbf
        self.byteLength = owner.params.byteLength

    def create_XOR_sums(self, players):
        self.indices = []
        for i in range(0, self.m):
            xor = int(0).to_bytes(self.byteLength, 'big')
            for index, player in enumerate(players):
                p_index = player.injective_function[i]

                # Player 0 uses its own messages
                if self.owner.id == 0:
                    m_index = (index * 2) + 1
                    m = self.owner.j_messages[p_index][m_index].message

                # Player 1 uses messages given to it
                else:
                    m_index = index
                    m = player.j_messages[p_index].message
               
                xor = helpers.xor_byte_array(xor, m)

            self.indices.append(xor)

    def get_GBF_XOR_sum(self, elem):
        xor_sum = int(0).to_bytes(self.byteLength, 'big')
        for i in range(0, self.hashes.count):
            j = self.hashes.getHash(i, elem)
            j = helpers.decfromdigest(j, self.m)
            k = self.indices[j]
            xor_sum = helpers.xor_byte_array(xor_sum, k)
        return xor_sum

def new(owner, hashes):
    return randomized_gbf(owner, hashes)