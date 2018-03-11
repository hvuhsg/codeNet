from threading import Thread
import socket
from time import sleep
from logs.log import log
from random import randint

server_log = log("logs\hack_game.log")

class server(object):
    def __init__(self, data, db):
        
        self.ip = data['address'][0]
        self.data = data
        self.db = db
        self.port = int(self.data["port"])
    
    def check_difend(self):
        Thread(target = self.guard_main).start()

    def guard_main(self):
        try:
            self.guard()
        except Exception as e:
            server_log.debug(str(type(e)) + ": " + str(e))

    def guard(self):
        sock = socket.socket()
        flag = True
        flag2 = False
        addr = (self.ip, self.port)
        
        for i in range(5):
            try:
                sock.connect(addr)
                flag2 = True
                break
            except:
                sleep(1)
        if not flag2:
            server_log.info("cant connect to " + str(addr))
            return
        else:
            server_log.info("connect to " + str(addr))

        lis = list(self.db.commend_list.items())
        num_of_commends = 5
        
        first = sock.recv(1024).decode()
        if "password" in first:
            sock.send(self.data['password'].encode())
            sock.recv(1024)

        for i in range(num_of_commends):
            a, b = lis[randint(0, len(lis)-1)]
            sock.send(a.encode())
            recv = sock.recv(1024).decode()
            if b != recv:
                flag = False
                break
        if flag:
            self.db.server_list.add(addr)
            sock.send(b"close")
            server_log.info("rgister sucsseful " + str(addr))
        else:
            server_log.info("rgister faild " + str(addr))
            sock.send(b"close")
        sock.close()

class meneger(object):
    def __init__(self, db):
        self.db = db
        Thread(target = self.run).start()

    def run(self):
        while not self.db.stop:
            del_set = set()
            try:
                for i in self.db.server_list:
                    s = socket.socket()
                    try:
                        s.connect(i)
                        s.close()
                    except ConnectionRefusedError:
                        del_set.add(i)
                        server_log.info("server disconnect " + str(i))
            except RuntimeError:
                pass
            for i in del_set:
                self.db.server_list.remove(i)
            sleep(3)
