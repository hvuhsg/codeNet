import time
from logs.log import log
from threading import Thread
from securty.EDY import EDY
from objects import user, server, group, errors, bot

class DB(object):
    def __init__(self, path):
        self.path = path
        self.stop = False
        self.old_db = None
        self.load_is_need = False
        self._db_log = log("logs\db_log.log")
        self._EDY = EDY

        self.commend_list = {"'a'":"a", "456":'456', "max(5, 9)":'9',
                             "print('hello')":"None", "eval('1+2')":'3',
                             "min(7, 5)":'5', '7+5':'12'}
        self.users = {}
        self._users_connect = {}
        self.errors = errors.LIST_OF_ERRORS
        
        self.server_list = set()
        server.meneger(self)

        self.groups = {}

        self.bots = {}
        self.public_bots_data = {}
        self.token = 0
        
        save_thread = Thread(target = self.save)
        load_thread = Thread(target = self.load)
        load_thread.start()
        save_thread.start()

    def save(self):
        print("Update data base prosses has begin.")
        while not self.stop:
            time.sleep(20)
            to_save = {}
            for a, b in self.__dict__.items():
                if a[0] != "_":
                    to_save[a] = b
            to_save = self.obj_to_dict(to_save)
            open(self.path, 'w').write(str(to_save))
            self._db_log.info("Data base was update.")

    def obj_to_dict(self, dic):
        new_dic = {}
        for a, b in dic.items():
            if type(b) == dict:
                new_dic[a] = self.obj_to_dict(b)
            else:
                try:
                    class_name = str(b)
                    if class_name:
                        class_name = class_name[class_name.find('.')+1:class_name.find(' ')]
                        new_dic[a] = (str(class_name), b.__dict__)
                    else:
                        class_name = str(type(b))
                        class_name = class_name[class_name.find('.')+1:class_name.rfind("'")]
                        new_dic[a] = (str(class_name), b.__dict__)
                except Exception as e:
                    new_dic[a] = b
        return new_dic

    def dict_to_obj(self, dic):
        new_dic = {}
        for a, b in dic.items():
            if type(b) == tuple:
                new_dic[a] = eval(b[0])()
                new_dic[a].__dict__ = b[1]
            elif type(b) == dict:
                new_dic[a] = self.dict_to_obj(b)
            else:
                new_dic[a] = b
        return new_dic
                

    def load(self):
        print("Load prooses has begin")
        flag = True
        while not self.stop:
            try:
                to_load = eval(open(self.path, 'r').read())
            except Exception as e:
                self._db_log.debug(str(e))
            if to_load['load_is_need'] == True or flag == True:
                to_load['load_is_need'] = False
                flag = False
                load_obj = self.dict_to_obj(to_load)
                self.__dict__.update(load_obj)
                print("Load data from data base.")
                self._db_log.info("Load data from data base.")
            time.sleep(9)

