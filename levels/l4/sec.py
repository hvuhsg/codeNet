﻿def sec(data):
    #Enter your code hear!
    #Exempel:
    if "pas" in data:
        return 1
    if "0" in data:
        return 1
    if "self" in data:
        return 1
    try:
        if eval(data) == get_password():
            return 1 #code is dengers
    except:
        pass
    return 0 #ok code is safe

#password to find
def get_password():
    return "1+1~3"

#serevr port
def get_port():
    return 4

#password connect user
def get_confirm_password():
    return "level4"

#big server ip
def get_server_ip():
    return "127.0.0.1"
