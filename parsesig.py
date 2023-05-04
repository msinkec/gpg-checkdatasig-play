#!/usr/bin/env python3

import hashlib
import attr
import io
import ecdsa
import json

import cashaddr
from minipgp import *

from sigstuff import verifies, compress, sigenc
from bitcoin import sha256

with open('pubkey.gpg', 'rb') as f:
    tagpaks = read_packets(f.read())

pubpak = PubKeyPacketV4.from_bytes(tagpaks[0][1])
assert(pubpak.oid.hex() == '2b8104000a')  ## make sure secp256k1
pubkey = pubpak.mpis[0].to_bytes(65,'big')
cpubkey = compress(pubkey)
assert(len(cpubkey) == 33)

vk = ecdsa.VerifyingKey.from_string(pubkey[1:], curve=ecdsa.SECP256k1, validate_point=True)
print("pubkey.gpg loaded, key ID", pubpak.key_id().hex().upper())
print()

# Extract the x and y coordinates of the public key point
x = vk.pubkey.point.x()
y = vk.pubkey.point.y()

# Print the coordinates
print("Public key point coordinates:")
print("x =", x)
print("y =", y)
print()

with open('testmsg', 'rb') as f:
    msg = f.read()
with open('testmsg.sig', 'rb') as f:
    _, (tag, sigpak) = read_packet(f.read())
    assert(tag == 2)
spme = SigPacketV4.from_bytes(sigpak)

assert(spme.sigtype == 0) # binary document
assert(spme.pubalgo == 19) # ECDSA
assert(spme.hashalgo == 8) # SHA256

# Calculate full hash
preimage = msg + spme.trailer()
digest = hashlib.sha256(preimage).digest()
hash2 = digest[:2]

assert hash2 == spme.hash2

print("Message:", repr(msg))
print("Message hex:", preimage.hex())
print()

r, s = spme.mpis
print("Sig:")
print("r:", r)
print("s:", s)
print()

print("Signature validity on message:", verifies(vk, digest, spme.mpis))
