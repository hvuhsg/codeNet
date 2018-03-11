
class MainError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def what(self):
        return(self.type_msg + ": " + self.msg)

class ServerError(MainError):
    pass

class ProtocolError(MainError):
    pass

class PremissionDenied(MainError):
    pass

class UserError(MainError):
    pass

class GroupError(MainError):
    pass

class NumberError(ProtocolError):
    def __init__(self):
        self.type_msg = "NumberError"
        super(type(self), self).__init__("The number of arguments is wrong.")
    def __call__(self, name = ""):
        return self

class NotConnect(UserError, PremissionDenied):
    def __init__(self):
        self.type_msg = "NotConnectError"
        super(type(self), self).__init__("Your not connected.")
    def __call__(self, name = ""):
        return self

class NameExsist(UserError):
    def __init__(self):
        self.type_msg = "NameExsistError"
        super(type(self), self).__init__("The name is alredy exsist on the system")
    def __call__(self, name = ""):
        self.msg = "The name %s is alredy exsist on the system"%name
        return self

class NotAdmin(GroupError, PremissionDenied):
    def __init__(self):
        self.type_msg = "NotAdminError"
        super(type(self), self).__init__("your not admin accses denied")
    def __call__(self, name = ""):
        self.msg = "your( %s ) not admin accses denied"%name
        return self

class ActionNotExsist(ProtocolError):
    def __init__(self):
        self.type_msg = "ActionNotExsist"
        super(type(self), self).__init__("action not exsist error")
    def __call__(self, name = ""):
        self.msg = "action %s not exsist error"%act
        return self

class UserNotInGroup(UserError, PremissionDenied):
    def __init__(self):
        self.type_msg = "UserNotInGroup"
        super(type(self), self).__init__("user not in group")
    def __call__(self, name = ""):
        self.msg = "user %s not in group"%name
        return self

class GroupNotExsist(GroupError):
    def __init__(self):
        self.type_msg = "GroupNotExsist"
        super(type(self), self).__init__("group name das not exsist")
    def __call__(self, name = ""):
        self.msg = "group %s das not exsist"%name
        return self

class UserNotExsist(UserError, GroupError):
    def __init__(self):
        self.type_msg = "UserNotExsist"
        super(type(self), self).__init__("user not exsist on the system")
    def __call__(self, name = ""):
        self.msg = "user ( %s ) not exsist on the system"%name
        return self

class DataError(ProtocolError):
    def __init__(self):
        self.type_msg = "DataError"
        super(type(self), self).__init__("invalid data")
    def __call__(self, data = ""):
        self.msg = "invalide data (%s)"%data
        return self

LIST_OF_ERRORS = {"number_error":NumberError(),
                  "not_connect":NotConnect(),
                  "name_exsist":NameExsist(),
                  "not_admin":NotAdmin(),
                  "act_not_exsist":ActionNotExsist(),
                  "user_not_in_group":UserNotInGroup(),
                  "group_not_exsist":GroupNotExsist(),
                  "user_not_exsist":UserNotExsist(),
                  "data_error":DataError()}

