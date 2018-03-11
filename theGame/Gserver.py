from threading import Thread
from client import clientY
import sec
import socket, time, sys

class serverY(object):
    def __init__(self):
        self.client = clientY()
        self.sr = socket.socket()
        self.port = sec.get_port()
        self.conf_password = sec.get_confirm_password()
        self.stop = False

    def register(self):
        self.client.connect((sec.get_server_ip(), 80))
        res = self.client.server_register(self.port, self.conf_password)
        self.client.close()
        return(res)
    
    def run_server(self):
        self.sr.bind(("0.0.0.0", self.port))
        self.sr.listen(1)
        while not self.stop:
            new_connect, addr = self.sr.accept()
            Thread(target = self.client_handeler, args = [new_connect]).start()
        print("end")
        self.sr.close()

    def client_handeler(self, sock):
        password = sec.get_password()
        try:
            if not self.confirm_password(sock):
                sock.close()
                return False
        except:
            sock.close()
        
        while True:
            try:
                recv = sock.recv(1000).decode()
                if not recv or recv == "close":
                    break
                res = self.run_code(recv)
                print(recv + ": " + res)
                sock.send(res.encode())
            except:
                break
        sock.close()

    def confirm_password(self, sock):
        if self.conf_password:
            sock.send(b"Enter password: ")
            recv = sock.recv(1024).decode()
            if not recv == self.conf_password:
                sock.send(b"WRONG PASSWORD")
                return False
            sock.send(b"OK PASSWORD")
        else:
            sock.send(b"welcome")
        return True

    def run_code(self, code):
        password = sec.get_password()
        if sec.sec(code):
            res = "Stop hacking"
        else:
            try:
                res = str(eval(code))
            except SyntaxError as e:
                try:
                    exec(code)
                    res = "None"
                except:
                    res = str(type(e)) + " " + str(e)
            except Exception as e:
                res = str(type(e)) + " " + str(e)
        return res

    def run(self):
        try:
            self.register()
        except:
            print("register error")
        a = Thread(target = self.run_server)
        a.start()

def test():
    server_obj = serverY()
    server_obj.run()
    #server_obj.stop = True

if __name__ == '__main__':
    test()
