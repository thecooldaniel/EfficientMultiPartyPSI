import protocol
import helpers
import hashes as h
import bloom_filter as bf
import garbled_bloom_filter as gbf

NumPlayers = 3 
PlayerInputSize = 5
Nbf = 20
SecParam = 20
Nmaxones = 10
bitLength = 128
p = 0.25
a = 0.3

Protocol = protocol.new(NumPlayers, Nmaxones, PlayerInputSize, p, a, SecParam, bitLength, Nbf)
Protocol.performRandomOT()
Protocol.getPlayerOnes()

ngbf = gbf.new(Protocol.params.Nbf, Protocol.params.PlayerInputSize, Protocol.params.bitLength, Protocol.hashes)
ngbf.add("testing")
ngbf.add(753)
ngbf.add("yessir")
ngbf.add("foobar")
r = helpers.int_to_string(ngbf.check("testing"))
r2 = ngbf.check(753)
r3 = helpers.int_to_string(ngbf.check("yessir"))
r4 = helpers.int_to_string(ngbf.check("foobar"))

a=1