from protocols.protocol import *

class servers_protocol(protocol):
    def __init__(self, db, log):
        self.actions = {"server_register":self.server_rgister,
                        "get_server_list":self.get_server_list}
        super(type(self), self).__init__(db, log)
    
    def server_rgister(self, data, sock):
        """act=server_register-!-port=<port>"""
        addr = data['address']
        _server = server(data, self.db)
        _server.check_difend()
        return "start rgister prosses"

    def get_server_list(self, data, sock):
        """act=get_server_list"""
        return "--"+str(self.db.server_list)
