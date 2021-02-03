'''
File For Trying Key Generation, signing transactions and verification
'''
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey

privateKey=PrivateKey()
publicKey=privateKey.publicKey()

msg="My Test Message"

signature=Ecdsa.sign(msg,privateKey)
verified=Ecdsa.verify(msg,signature,publicKey)
print(verified)