import socket, select, random, time
from protocol import protocol
import securty.EDY as EDY
from logs.log import log
from securty.RSA import _rsa

class server(object):
    def __init__(self, port):
        self.socket_list = []
        self.port = port

        self.main_socket = socket.socket()
        self.main_socket.bind(('0.0.0.0', port))
        self.main_socket.listen(10)
        
        self.users_data = {}
        self.protocol = protocol()
        self.server_log = log("logs\server.log")

        self.address_of_sockets = {}
        
    def run(self):
        while True:
            time.sleep(0.01)
            rlist, wlist, xlist = select.select([self.main_socket] + self.socket_list, self.socket_list, [])
            for current_socket in rlist:
                if current_socket is self.main_socket:
                    (new_socket, address) = self.main_socket.accept()
                    self.socket_list.append(new_socket)
                    self.server_log.info("connect: " + str(address))
                    try:
                        _rsa.sequre_connection(new_socket)
                    except ConnectionResetError:
                        print("Connection with client closed.")
                    self.users_data[new_socket] = ''
                    self.address_of_sockets[new_socket] = address
                else:
                    try:
                        data = current_socket.recv(10000)
                        try:
                            self.users_data[current_socket] = data.decode()
                        except:
                            self.users_data[current_socket] = data
                        if not data:
                            raise ConnectionAbortedError
                    except:
                        try:
                            self.protocol.db._users_connect.pop(current_socket)
                        except:
                            pass
                        self.socket_list.remove(current_socket)
                        print("Connection with client closed.")
            self.send_waiting_messages(wlist)
    
    def send_waiting_messages(self, wlist):
        for i in wlist:
            if not self.users_data[i]:
                continue
            try:
                decrypt = self.decrypt(i, self.users_data[i])
            except Exception as e:
                if i in self.protocol.db._users_connect.keys():
                    self.server_log.debug(self.get_user(i) + "decrypt data")
                    i.send(b'decrypt error')
                    self.users_data[i] = ''
                    continue
                else:
                    decrypt = self.users_data[i]
            protocol = self.protocol(decrypt, i, self.address_of_sockets[i])
            if issubclass(type(protocol), Exception):
                protocol = protocol.what()
            try:
                to_send = self.encrypt(i, protocol)
            except Exception as e:
                 self.server_log.debug(str(type(e)) + self.get_user(i) + "encrypt data: " + str(e))
            try:
                i.send(to_send)
            except Exception as e:
                 self.server_log.debug(str(type(e)) + self.get_user(i) + "send error")
            self.users_data[i] = ''

    def encrypt(self, socket, data):
        try:
            self.protocol.db._users_connect[socket]
            if data[:2] == "--":
                data = data[2:]
                raise "dont encrypt thet!"
        except:
            return data.encode()
        ed = EDY.EDY(self.protocol.db._users_connect[socket].password)
        data = str(ed.en(data))
        return data.encode()

    def decrypt(self, socket, data):
        try:
            data = _rsa.decrypt(data)
        except Exception as e:
            raise
        return data

    def get_user(self, sock):
        try:
            return 'name: ' + self.protocol.db._users_connect[sock].name + ' '
        except:
            return 'name: unknow '

def main():
    my_server = server(80)
    my_server.run()
main()
