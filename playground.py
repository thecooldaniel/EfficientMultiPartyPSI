# import hashlib

# def injective(index, domain):
#     m = hashlib.sha256(index.encode())
#     n = m.hexdigest()
#     dec = int(n, 16)
#     return dec % domain

# # 962128136439002204627086364833379305114492637063779668990484275351240916102
# # NBF = 1000
# # print( injective("2", 1000) )


# # NBF = 512
# # Not - C = 245

# # BF = [0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0]

# BF[6] = 0
# g[6] == 0

# BF[1...NBF] = l
# g[1...NBF] == l
# # print(BF[9])
# # print(BF[9 % 20])
