from protocols.protocol import *

class users_protocol(protocol):
    def __init__(self, db, log):
        self.actions = {'sing_in':self.sing_in,
                        'sing_out':self.sing_out,
                        'register':self.register,
                        "get":self.get,
                        'set':self.set}
        super(users_protocol, self).__init__(db, log)

    def sing_in(self, data, sock):
        '''act=sing_in-!-name=<name>-!-password=<password>'''
        name = data['name']
        password = data['password']
        try:
            self.db.users[name]
        except:
            return self.db.errors['user_not_exsist']
        if self.db.users[name].password == password:
            if self.db.users[name].is_close == False:
                self.db._users_connect[sock] = self.db.users[name]
            else:
                return self.db.errors['user_is_close']
        else:
            return self.db.errors['password_error']
        return 'OK connect.'

    def sing_out(self, data, sock):
        '''act=sing_out'''
        try:
            self.db._users_connect.pop(sock)
        except:
            return self.db.errors['not_connect']
        return 'OK disconnect'

    def register(self, data, sock):
        '''act=register-!-name=<name>-!-password=<password>'''
        name = data['name']
        password = data['password']
        ed = self.db._EDY(password)
        try:
            self.db.users[name]
            return self.db.errors['name_exsist']
        except:    
            self.db.users[name] = user(name, password)
            self.sing_in(data, sock)
        return 'OK register'

    def get(self, data, sock):
        '''act=get-!-folder=<name_of_folder>'''
        try:
            self.db._users_connect[sock]
        except:
            return self.db.errors['not_connect']
        if data['folder'] == 'all':
            res = str(self.db._users_connect[sock].folder)
            return res
        return self.db._users_connect[sock].folder[data['folder']]

    def set(self, data, sock):
        '''act=get-!-folder=<name_of_folder>-!-data=<data_to_save>'''
        try:
            self.db._users_connect[sock]
        except:
            return self.db.errors['not_connect']
        self.db._users_connect[sock].folder[data['folder']] = data['data']
        return 'ok set'
        
