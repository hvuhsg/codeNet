def sec(data):
    #Enter your code hear!
    #Exempel:
    if "pas" in data:
        return 1
    if "exec" in data or "eval" in data:
        return 1
    if "self" in data:
        return 1
    if "open" in data or "=" in data:
        return 1
    if "0" in data:
        return 1
    if "import" in data:
        return 1
    try:
        if eval(data) == get_password():
            return 1 #code is dengers
    except:
        pass
    return 0 #ok code is safe

#password to find
def get_password():
    return "finish"

#serevr port
def get_port():
    return 6

#password connect user
def get_confirm_password():
    return "greet job"

#big server ip
def get_server_ip():
    return "127.0.0.1"
