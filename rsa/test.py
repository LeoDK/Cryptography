from rsa import Crypto

#c = Crypto(key=(33, 3, 7))
c = Crypto(n_bits=64)
print("e : ", c.e)
print("d : ", c.d)
print("n : ", c.n)

msg = 23
print( "encrypted : ", c.encrypt(msg) )
print( "decrypted : ", c.decrypt(c.encrypt(msg)) )
