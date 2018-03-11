
class bot(object):
    def __init__(self, bot_name = "", admin = ""):
        self.admin = admin
        self.users = set()
        self.black_list = []
        self.commends = {}

    def add_commend(self, key, value):
        self.commends[key] = value

    def remove_commnend(self, key):
        self.commends.pop(key)

    def register(self, user_name):
        if not user_name in black_list:
            self.users.add(user_name)

    def keek_user(self, user_name):
        self.users.remove(user_name)
        self.black_list.append(user_name)

    def sign_out(self, user_name):
        self.users.remove(user_name)

    def in_bot(self, user_name):
        return user_name in self.users

    def is_admin(self, user_name):
        return user_name == self.admin

    
        

        
