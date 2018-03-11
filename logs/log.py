import time

class log(object):
    def __init__(self, filename):
        self.filename = filename

    def write(self, data):
        try:
            open(self.filename, 'a').write(data)
        except FileExistsError:
            file = open(self.filename, 'w')
            file.close()
            self.write(data)

    def time(self):
        return "time: " + str(time.time()) + ' '

    def info(self, data):
        type_log = "INFO: "
        self.write(type_log + self.time() + data + '\n')

    def debug(self, data):
        type_log = "DEBUG: "
        self.write(type_log + self.time() + data + '\n')
    
    
