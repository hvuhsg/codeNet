def sec(data):
    #Enter your code hear!
    #Exempel:
    if "pas" in data:
        return 1
    if "eval" in data:
        return 1
    try:
        if eval(data) == get_password():
            return 1 #code is dengers
    except:
        pass
    return 0 #ok code is safe

#password to find
def get_password():
    return "1+1~7"

#serevr port
def get_port():
    return 2

#password connect user
def get_confirm_password():
    return "abct"

#big server ip
def get_server_ip():
    return "127.0.0.1"
