def sec(data):
    #Enter your code hear!
    #Exempel:
    if "password" in data:
        return 1
    if "self" in data:
        return 1
    return 0 #ok code is safe

#password to find
def get_password():
    return "GOOD FOR YOU"

#serevr port
def get_port():
    return 27

#password connect user
def get_confirm_password():
    return ""

#big server ip
def get_server_ip():
    return "127.0.0.1"
