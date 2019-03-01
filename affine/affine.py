def eucl (a, b):
    """
    Retourne un couple (u,v) tq au+bv = pgcd(a,b).
    Peut être prouvé par récurrence sur n, où pour tout n, aun + bvn = rn.
    """
    u0, v0, u1, v1 = 1, 0, 0, 1
    while b!=0:
        q = a/b
        a, b, u0, v0, u1, v1 = b, a%b, u1, v1, u0 - q*u1, v0 - q*v1
    return (u0, v0)

def invMod (x, n):
    return eucl(x, n)[0]

def pgcd (a, b):
    while b!=0:
        a, b = b, a%b
    return a


N_CHAR_DEF = 26
CHAR_BEGIN_DEF = ord("a")

class Crypto (object):

    def __init__ (self, a, b, N_CHAR = N_CHAR_DEF, CHAR_BEGIN = CHAR_BEGIN_DEF):
        self.N_CHAR = N_CHAR
        self.CHAR_BEGIN = CHAR_BEGIN
        if pgcd(a, self.N_CHAR) != 1:
            raise Exception("a et 26 doivent être premiers entre eux.")

        self.a = a
        self.b = b
        self.c = invMod(a, self.N_CHAR)
        self.d = N_CHAR - self.c*self.b

    def encrypt (self, msg):
        ret = []
        for l in msg:
            ret.append( chr(self.CHAR_BEGIN + (self.a*(ord(l)-self.CHAR_BEGIN) + self.b)%self.N_CHAR) )
        return "".join(ret)

    def decrypt (self, msg):
        ret = []
        for l in msg:
            ret.append( chr(self.CHAR_BEGIN + (self.c*(ord(l)-self.CHAR_BEGIN) + self.d)%self.N_CHAR) )
        return "".join(ret)
