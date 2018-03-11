
class group(object):
    def __init__(self, name = ''):
        self.name = name
        self.users = []
        self.admins = []
        self.proj = {}

    def add_user(self, name):
        if not self.in_group(name):
            self.users.append(name)

    def remove_user(self, name):
        self.users.remove(name)
        if self.is_admin(name):
            self.admins.remove(name)

    def make_admin(self, name):
        if not name in self.admins:
            self.admins.append(name)

    def in_group(self, name):
        return name in self.users

    def is_admin(self, name):
        return name in self.admins

    def len_users(self):
        return len(self.users)
    
    def set(self, key, value):
        self.proj[key] = value

    def get(self, key):
        if key == "all":
            return str(self.proj)
        return self.proj[key]
            
