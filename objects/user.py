class user(object):
    def __init__(self, name = '', password = ''):
        self.name = name
        self.password = password
        self.is_close = False
        self.folder = {}
        
