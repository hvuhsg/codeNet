from protocols.protocol import *


class groups_protocol(protocol):
    def __init__(self, db, log):
        self.actions = {"new_group":self.new_group,
                        "add_user":self.add_user,
                        "remove_user":self.remove_user,
                        "make_admin":self.make_admin,
                        "set_group":self.set,
                        "get_group":self.get}
        super(type(self), self).__init__(db, log)

    def new_group(self, data, sock):
        """act=new_group-!-name=<group_name>"""
        try:
            user_name = self.db._users_connect[sock]
        except:
            res = self.db.errors["not_connect"]
            return res
        try:
            name = data['name']
        except:
            return self.db.errors['data_error'](data)
        new_group = group(name)
        new_group.add_user(user_name.name)
        new_group.make_admin(user_name.name)
        self.db.groups[name] = new_group
        return "ok group created."

    def add_user(self, data, sock):
        """act=add_user-!-name=<user_to_add>-!-group=<group_name>"""
        res = self.chack_global(data, sock)
        if type(res) == tuple:
            user_name, group = res
        else:
            return res
        try:
            name = data['name']
            self.db.users[name]
        except:
            return self.db.errors['user_not_exsist'](name)

        group_name = data['group']        
        if not group.is_admin(user_name):
            return self.db.errors['not_admin'](user_name)
        group.add_user(data['name'])
        return "ok " + data['name'] + " was add to group " + group_name

    def remove_user(self, data, sock):
        """act=remove_user-!-name=<user_to_remove>-!-group=<group_name>"""
        res = self.chack_global(data, sock)
        if type(res) == tuple:
            user_name, group = res
        else:
            return res
        try:
            name = data['name']
            self.db.users[name]
        except:
            return self.db.errors['user_not_exsist'](name)

        group_name = data['group']
        if not (group.is_admin(user_name) or user_name == name):
            return self.db.errors['not_admin'](user_name)
        if not group.in_group(data['name']):
            return self.db.errors['user_not_in_group'](data['name'])
        group.remove_user(data['name'])
        if group.len_users() == 0:
            self.db.groups.pop(group.name)
        return "ok " + data['name'] + " was remove from group " + group_name

    def make_admin(self, data, sock):
        """act=make_admin-!-name=<user_to_make_admin>-!-group=<group_name>"""
        res = self.chack_global(data, sock)
        if type(res) == tuple:
            user_name, group = res
        else:
            return res
        try:
            name = data['name']
            self.db.users[name]
        except:
            return self.db.errors['user_not_exsist'](name)
        
        if not group.is_admin(user_name):
            return self.db.errors['not_admin'](user_name)
        if not group.in_group(data['name']):
            return self.db.errors['user_not_in_group'](data['name'])
        group.make_admin(data['name'])
        return "ok " + data['name'] + " is admin now"

    def set(self, data, sock):
        """act=set_group-!-group=<group_name>-!-folder=<folder_name>-!-data=<data_to_save>"""
        res = self.chack_global(data, sock)
        if type(res) == tuple:
            user_name, group = res
        else:
            return res
        
        if not group.in_group(user_name):
            return self.db.errors["user_not_in_group"](user_name)
        group.set(data['folder'], data['data'])
        return "ok data set"

    def get(self, data, sock):
        """act=get_group-!-group=<group_name>-!-folder=<folder_name>"""
        res = self.chack_global(data, sock)
        if type(res) == tuple:
            user_name, group = res
        else:
            return res
        
        if not group.in_group(user_name):
            return self.db.errors["user_not_in_group"](user_name)
        data = group.get(data['folder'])
        return data

    def chack_global(self, data, sock):
        try:
            user_name = self.db._users_connect[sock]
            user_name = user_name.name
        except:
            return self.db.errors["not_connect"]()
        try:
            group_name = data['group']
            group = self.db.groups[group_name]
        except:
            return self.db.errors['group_not_exsist'](group_name)
        return (user_name, group)
        
        
    
