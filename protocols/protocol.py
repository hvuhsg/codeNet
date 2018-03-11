from objects.user import user
from objects.server import server
from objects.group import group
from objects.bot import bot

class protocol(object):
    def __init__(self, db, log):
        self.db = db
        self.log = log

    def __call__(self, data, sock):
        if not data['act'] in self.actions.keys():
            return False
        else:
            #try:
            return self.actions[data['act']](data, sock)
            #except Exception as e:
             #   self.log.debug(str(type(e)) + " " + str(e))
              #  return self.db.errors['data_error'](data)
    
                
