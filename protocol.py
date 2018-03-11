from logs.log import log
import DB

from protocols.users_protocol import users_protocol
from protocols.servers_protocol import servers_protocol
from protocols.groups_protocol import groups_protocol
from protocols.bots_protocol import bots_protocol

class protocol(object):
    def __init__(self):
        self.db = DB.DB(r'DB\dby.db')

        self.main_log = log('logs\protocol.log')

        self.protocols = [users_protocol(self.db, self.main_log),
                          servers_protocol(self.db, self.main_log),
                          groups_protocol(self.db, self.main_log),
                          bots_protocol(self.db, self.main_log)]

    def to_dict(self, data, sock, addr):
        if type(data) == bytes:
            data = data.decode()
        data = data.split('-!-')
        data = [i.split('=') for i in data]
        new_data = {}
        for i in data:
            new_data[i[0]] = i[1]
        try:
            sock = self.db._users_connect[sock].name
        except:
            sock = 'unknow'
        self.main_log.info("recv_from: " + str(sock) + ' data: ' + str(new_data))
        print(sock, new_data)
        new_data["address"] = addr
        return new_data

    def __call__(self, data, sock, addr):
        try:
            data = self.to_dict(data, sock, addr)
        except Exception as e:
            self.main_log.debug('data_error ' + str(type(e)) + " " + str(e))
            return self.db.errors["data_error"](data)
        for i in self.protocols:
            res = i(data, sock)
            if res:
                break
        if not res:
            res = self.db.errors["act_not_exsist"]
        if issubclass(type(res), Exception):
            res = res.what()
        try:
            sock = self.db._users_connect[sock].name
        except:
            sock = 'unknow'
        self.main_log.info("send_to: " + str(sock) + ' data: ' + str(res))
        return res
