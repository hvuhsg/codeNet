from hashlib import shake_256
import time

class EDY(object):
    def __init__(self, password):
        self.strong = 10
        self.keys = []
        self.new_keys(password, self.strong)
        self.range_of_chars = 255
        self.k3 = self.my_hash(self.keys[0][0], self.keys[1][0])

    def new_keys(self, password, strong):
        num = 190
        has = shake_256()
        has.update(password.encode())
        hex_dig = has.hexdigest(num*strong*2)
        for i in range(strong):
            k1 = self.get_num(hex_dig[i*num:(i+1)*num])
            k2 = self.get_num(hex_dig[i*num*2:(i+1)*num*2])
            key = (k1, k2)
            self.keys.append(key)

    def get_num(self, st):
        num = 0
        for i in st:
            num += ord(i)
        return num

    def my_hash(self, num, num_of_digest):
        hk3 = shake_256()
        hk3.update(str(num).encode())
        k3 = self.get_num(hk3.hexdigest(num_of_digest))
        return k3

    def g(self, n, k1):
        e = (n**k1) % self.k3
        return e, self.my_hash((e+n*12345)%k1, 30)

    def en_hard(self, st, k1):
        ans = []
        for i in st:
            i = ord(i)
            ans.append(self.g(i, k1))
        return(ans)

    def dg(self, e, he, k1):
        for i in range(0, self.range_of_chars):
            if (i**k1) % self.k3 == e:
                if self.my_hash((e+i*12345)%k1, 30) == he:
                    return(i)

    def de_hard(self, data, k1):
        st = 0
        for e, he in data:
            st += self.dg(e, he, k1)
        return st

    def en(self, st):
        ans = []
        password = 0
        hard_points = 0
        for i in st:
            if hard_points < self.strong:
                password += ord(i)
                ans.append(self.en_hard(i, self.keys[hard_points][0]))
                hard_points += 1
            else:
                i = ord(i)
                ans.append((i + password) % 255)
                password = i
        return ans

    def de(self, data):
        st = ""
        password = 0
        count = 0
        for i in data:
            if type(i) == list:
                ans = self.de_hard(i, self.keys[count][0])
                password += ans
                count += 1
                st += chr(ans)
            else:
                ans = (i - password) % 255
                st += chr(ans)
                password = ans
        return st

    def hack(self, data):
        st = ""
        password = 0
        for i in data:
            if type(i) == list:
                ans = self.hack_de_hard(i)
                print(ans)
                password += ans
                st += chr(ans)
            else:
                ans = (i - password) % 255
                st += chr(ans)
                password = ans
        return st

    def hack_de_hard(self, data):
        t = time.time()
        for e, he in data:
            for j in range(13000, 21000):
                for j2 in range(20000, 21000):
                    if j2 % 100 == 0:
                        print(time.time() - t)
                    for i in range(0, self.range_of_chars):
                        if (i**j) % j2 == e:
                            if self.my_hash(e+j, 30) == he:
                                return(i)
                

def test():
    ed = EDY("aseew***")
    ed2 = EDY("12#$%68*3ww")
    data2 = ed.en('hello world!!')
    data = ed.en('jahsg*-*/ghsd')
    print("encrypt:", data)
    print("encrypt2:", data2)
    t1 = time.time()
    print(ed.de(data))
    print(ed.de(data2))
    print(time.time() - t1)
    input()

if __name__ == "__main__":
    test()
