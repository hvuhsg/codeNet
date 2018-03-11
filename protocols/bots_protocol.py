from protocols.protocol import *

class bots_protocol(protocol):
    def __init__(self, db, log):
        self.actions = {"bot_register":self.add_user,
                        "new_bot":self.new_bot,
                        "bot_add_commend":self.add_commend,
                        "bot_asking":self.bot_asking}
        super(type(self), self).__init__(db, log)

    def global_check(self, data, sock):
        try:
            user_name = self.db._users_connect[sock].name
        except:
            return self.db.errors['not_connect'], None
        try:
            bot_name = data['bot_name']
        except:
            return self.db.errors["data_error"](data), None
        return user_name, bot_name

    def new_bot(self, data, sock):
        user_name, bot_name = self.global_check(data, sock)
        if type(user_name) != str:
            return user_name
        self.db.bots[bot_name] = bot(bot_name, user_name)
        return "ok create bot"

    def add_user(self, data, sock):
        user_name, bot_name = self.global_check(data, sock)
        if type(user_name) != str:
            return user_name
        self.db.bots[bot_name].register(user_name)
        return "ok register"

    def add_commend(self, data, sock):
        user_name, bot_name = self.global_check(data, sock)
        if type(user_name) != str:
            return user_name
        try:
            key, value = data['key'], data['value']
        except:
            return self.db.errors['data_error'](data)
        if self.db.bots[bot_name].is_admin(user_name):
            self.db.bots[bot_name].add_commend(key, value)
        return "ok commend adding"

    def bot_asking(self, data, sock):
        user_name, bot_name = self.global_check(data, sock)
        if type(user_name) != str:
            return user_name
        try:
            ask = data['ask']
        except:
            return self.db.error['data_error'](str(data) + "hello")
        return self.db.bots[bot_name].commends[ask]

        
