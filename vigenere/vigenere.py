class Crypto (object):

    def __init__ (self, key):
        self.key = key

    def encrypt (self, msg):
        ret = []
        for i in range(len(msg)):
            ret.append( chr(ord("a") + (ord(msg[i])-ord("a") + ord(self.key[i%len(self.key)]))%26) )
        return "".join(ret)

    def decrypt (self, msg):
        ret = []
        for i in range(len(msg)):
            ret.append( chr(ord("a") + (ord(msg[i])-ord("a") - ord(self.key[i%len(self.key)]))%26) )
        return "".join(ret)

c = Crypto("clef")
out = c.encrypt("coucou")
print(out)
print(c.decrypt(out))
