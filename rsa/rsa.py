import struct
from math import sqrt
from random import randrange

def modPow (a, e, n):
    """ a**e mod n en exponentiation rapide """
    res = 1
    while e > 0:
        if e & 1 == 1:
            res = (res*a)%n
        e >>= 1
        a = (a*a)%n
    return res

def millerWitness (a, n, s, d):
    """ Cf démo sur wikipedia """
    x = modPow(a, d, n)
    if x == 1 or x == n-1:
        return False
    while s > 1:
        x = modPow(x, 2, n)
        if x == n-1:
            return False
        s -= 1
    return True

def isPrime (n, k=1000):
    """
    Test de primalité de Miller-Rabin.
    """
    # On cherche s,d tq n-1 = 2^s * d
    s = 0
    d = n-1
    while d%2 == 0:
        s += 1
        d //= 2

    tested = []
    for i in range(k):
        a = randrange(2, n)
        while a in tested and len(tested)<n-3:
            a = randrange(2, n)
        tested.append(a)
        if millerWitness(a, n, s, d):
            return False

    return True

def getRand (n_bits):
    """
    Reading in /dev/urandom (in linux systems).
    """
    n = 3
    with open("/dev/urandom", "rb") as f:
        for i in range(int(n_bits/8)):
            rand_char = struct.unpack("B", f.read(1))[0]
            n += (rand_char << (8*i))
    return n

def genLargePrime (n_bits):
    p = getRand(n_bits)
    while not isPrime(p):
        p = getRand(n_bits)
    return p

def gcd (a, b):
    """ pgcd """
    while b != 0:
        a, b = b, a%b
    return a

def genLargeRelPrime (a, n_bits):
    b = getRand(n_bits)
    while gcd(a,b) != 1:
        b = getRand(n_bits)
    return b

def eucl (a, b):
    """
    Euclide étendu : trouver un couple (u,v) tq au+bv = pgcd(a,b).
    """
    u0, v0, u1, v1 = 1, 0, 0, 1
    while b!=0:
        q = a//b
        a, b, u0, v0, u1, v1 = b, a%b, u1, v1, u0 - q*u1, v0 - q*v1
    return (u0, v0)

def modInv (a, n):
    """
    Inverse modulaire (n'existe que si a et n premiers entre eux).
    """
    res = eucl(a, n)[0]
    if res < 0:
        res = a * modPow(res, 2, n)
    return res

class Crypto (object):

    # Clé : (n, e, d)
    EMPTY_KEY = (0,0,0)
    DEF_BITS = 512

    @staticmethod
    def genKey (n_bits):
        p = genLargePrime(n_bits)
        q = genLargePrime(n_bits)
        print("p=",p)
        print("q=",q)
        n = p*q
        phi = (p-1)*(q-1)
        e = genLargeRelPrime(phi, n_bits)
        d = modInv(e, phi)%phi
        return (n, e, d)

    def __init__ (self, key=EMPTY_KEY, n_bits=DEF_BITS):
        if key != Crypto.EMPTY_KEY:
            self.n, self.e, self.d = key
        else:
            self.n, self.e, self.d = Crypto.genKey(n_bits)
        self.pubkey = (self.n, self.e)
        self.privkey = (self.n, self.d)

    def encrypt (self, m):
        return modPow(m, self.e, self.n)

    def decrypt (self, c):
        return modPow(c, self.d, self.n)
