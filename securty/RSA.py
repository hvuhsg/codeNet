import rsa

class RSA(object):
    def __init__(self, privet_key):
        self.pri = privet_key
        self.pub = rsa.PublicKey(self.pri.n, self.pri.e)

    def decrypt(self, msg):
        return rsa.decrypt(msg, self.pri).decode()

    def encrypt(self, msg):
        return rsa.encrypt(msg.encode(), self.pub)

    def sign(self, msg):
        return rsa.sign(msg, self.pri, "SHA-256")

    def verifly(self, msg, sign):
        return rsa.verify(msg.encode(), sign, self.pub)

    def sequre_connection(self, sock):
        msg = (str(self.pub.n) + ":" + str(self.pub.e) + ":").encode()
        sock.send(b"send random string")
        rand = sock.recv(5000)
        msg += rand
        msg += b":" + self.sign(msg)
        sock.send(msg)
         
try:
    priv_key = open(r"securty\priv_key.key", 'r').read()
except:
    priv_key = open(r"priv_key.key", 'r').read()
priv_key = priv_key.encode()
priv_key = rsa.PrivateKey.load_pkcs1(priv_key)

_rsa = RSA(priv_key)
