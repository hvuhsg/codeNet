import unittest
from RSA import _rsa
from EDY import EDY
from random import randint

class securtyTest(unittest.TestCase):

    def test_encrypt_decrypt(self):
        self.assertEqual(_rsa.decrypt(_rsa.encrypt("test")), "test")

    def test_sign_verfly(self):
        self.assertTrue(_rsa.verifly("hello", _rsa.sign(b"hello")))

    def test_encrypt_decrypt_edy(self):
        ch = "1234567890-=qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASGHJKLZXCVBNM,"
        for i in range(3):
            st = "".join([ch[randint(0, len(ch)-1)] for i in range(5)])
            self.test_one_itral(st)

    def test_one_itral(self, st = "asd"):
        edy = EDY(st)
        self.assertEqual(edy.de(edy.en(st)), st)

if '__main__' == __name__:
    unittest.main()
