class admin(object):
    def __init__(self):
        self.db = {}
        self.path = r"DB\dby.db"
        self.path_backup = r"DB\backup.db"
        #self.path, self.path_backup = self.path_backup, self.path
    
    def load(self):
        self.db = eval(open(self.path, 'r').read())
    
    def save(self):
        open(self.path, 'w').write(str(self.db))
    
    def show(self, name, num = 1):
        for a, b in name.items():
            if type(b) == dict:
                print('    '*num,a)
                self.show(b, num+1)
            elif type(b) == tuple:
                print("    "*num, a)
                for i in b:
                    if type(i) == dict:
                        self.show(i, num+1)
                    else:
                        print("    "*num, i)
            else:
                print("    "*num, a, b)

    def close_user(self, name):
        self.db['users'][name][1]['is_close'] = True

    def backup(self):
        open(self.path_backup, 'w').write(str(self.db))

    def load_backup(self):
        self.db = eval(open(self.path_backup, 'r').read())

ad = admin()
ad.load()
def main():
    while 1:
        cod = input('>>>')
        if cod == "exit" or cod == 'end':
            ad.save()
            break
        else:
            try:
                exec('ad.'+cod)
            except:
                try:
                    exec(cod)
                except:
                    print("Error")
main()
