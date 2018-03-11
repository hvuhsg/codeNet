import socket, time
import rsa
from random import randint
from securty.EDY import EDY
from threading import Thread

class clientY(object):
    def __init__(self):
        self.s = socket.socket()
        self.ed = None
        self.rsa_pub_key = None

    def en(self, data):
        return str(self.ed.en(data))

    def de(self, data):
        if not "[" in data:
            return data
        return self.ed.de(eval(data))
    
    def randstr(self):
        chars = "1234567890zsdfghjlasdn,nbca*ADFDFGTRRDSDKJMHN-.,"
        st = ""
        for i in range(30):
            st += chars[randint(0, len(chars)-1)]
        return st
    
    def connect(self, address):
        self.s.connect(address)
        self.s.recv(1024)
        randst = self.randstr()
        self.s.send(randst.encode())
        
        pub_key = self.s.recv(50000)
        if not randst.encode() in pub_key:
            print("sequre error")

        return (self.secure_connect(pub_key))

    def secure_connect(self, pub_key):
        pub_key2 = pub_key[:]
        pub_key2 = pub_key2[pub_key2.find(b":")+1:]
        pub_key2 = pub_key2[pub_key2.find(b":")+1:]
        pub_key2 = pub_key2[pub_key2.find(b":")+1:]
        sign = pub_key2

        pub_key = pub_key[:pub_key.find(pub_key2)-1]
        pub_key_str = pub_key.split(b":")
        self.rsa_pub_key = rsa.PublicKey(int(pub_key_str[0]), int(pub_key_str[1]))

        boolean = False
        try:
            boolean = rsa.verify(pub_key, sign, self.rsa_pub_key)
        except:
            pass
        return boolean

    def send(self, data):
        if type(data) == str:
            data = data.encode()
        self.s.send(rsa.encrypt(data, self.rsa_pub_key))

    def recv(self, num):
        return self.de(self.s.recv(num).decode())
    
    def register(self, name, password):
        self.ed = EDY(password)
        to_send = ("act=register-!-name=%s-!-password=%s"%(name, password)).encode()
        self.send(to_send)
        return self.recv(5000)

    def sing_in(self, name, password):
        self.ed = EDY(password)
        to_send = ("act=sing_in-!-name=%s-!-password=%s"%(name, password)).encode()
        self.send(to_send)
        return self.recv(5000)

    def set(self, folder, data):
        to_send = ("act=set-!-folder=%s-!-data=%s"%(folder, data)).encode()
        self.send(to_send)
        return self.recv(5000)
    
    def get(self, folder):
        to_send = ("act=get-!-folder=%s"%(folder)).encode()
        self.send(to_send)
        return self.recv(5000)

    def get_group(self, group, folder):
        to_send = ("act=get_group-!-group=%s-!-folder=%s"%(group, folder)).encode()
        self.send(to_send)
        return self.recv(5000)
    
    def set_group(self, group, folder, data):
        to_send = ("act=set_group-!-group=%s-!-folder=%s-!-data=%s"%(group, folder, data)).encode()
        self.send(to_send)
        return self.recv(5000)

    def sing_out(self):
        to_send = b"act=sing_out"
        self.send(to_send)
        res = self.recv(5000)
        return res

    def server_register(self, port, password = ''):
        to_send = "act=server_register-!-port=%d-!-password=%s"%(port, password)
        self.send(to_send)
        return self.s.recv(1024).decode()

    def get_server_list(self):
        to_send = b"act=get_server_list"
        self.send(to_send)
        return self.s.recv(5000).decode()

    def new_group(self, name):
        to_send = "act=new_group-!-name=%s"%name
        self.send(to_send)
        res = self.recv(5000)
        return res

    def add_user(self, group, name):
        to_send = "act=add_user-!-name=%s-!-group=%s"%(name, group)
        self.send(to_send)
        res = self.recv(5000)
        return res

    def remove_user(self, group, name):
        to_send = "act=remove_user-!-name=%s-!-group=%s"%(name, group)
        self.send(to_send)
        res = self.recv(5000)
        return res

    def make_admin(self, group, name):
        to_send = "act=make_admin-!-name=%s-!-group=%s"%(name, group)
        self.send(to_send)
        res = self.recv(5000)
        return res

    def new_bot(self, bot_name):
        to_send = "act=new_bot-!-bot_name=%s"%bot_name
        self.send(to_send)
        res = self.recv(5000)
        return res

    def bot_register(self, bot_name):
        to_send = "act=bot_register-!-bot_name=%s"%bot_name
        self.send(to_send)
        res = self.recv(5000)
        return res

    def bot_add_commend(self, bot_name, key, value):
        to_send = "act=bot_add_commend-!-bot_name=%s-!-key=%s-!-value=%s"%(bot_name, key, value)
        self.send(to_send)
        res = self.recv(5000)
        return res

    def bot_asking(self, bot_name, ask):
        to_send = "act=bot_asking-!-bot_name=%s-!-ask=%s"%(bot_name, ask)
        self.send(to_send)
        res = self.recv(5000)
        return res
        
    def close(self):
        self.s.close()

        
def create_random_id():
    chars = "1234567890qwertyuiopasdfghjklzxcvbnm"
    password = "".join([chars[randint(0, len(chars)-1)] for i in range(10)])
    name = "".join([chars[randint(0, len(chars)-1)] for i in range(10)])
    return(name, password)

def test():
    for i in range(1):
        client = clientY()
        if not client.connect(("127.0.0.1", 80)):
            continue
        print("connected.\n")
        
        name, password = create_random_id()
        folder, data = create_random_id()
        user = name
        print(client.register(name, password))
        print(client.set(folder, data))
        print(client.get(folder))
        
        print(client.new_group(data))
        print(client.add_user(data, user))
        print(client.make_admin(data, user))
        print(client.set_group(data, "test_set", "good_get"))
        print(client.get_group(data, "test_set"))
        print(client.remove_user(data, user))
        
        print(client.new_bot("new_bot"))
        print(client.bot_add_commend("new_bot", "hello", "hello you how you doing?"))
        print(client.bot_asking("new_bot", "hello"))
        
        print(client.sing_out())
        client.close()

if '__main__' == __name__:
    for i in range(1):
        Thread(target = test).start()

    

