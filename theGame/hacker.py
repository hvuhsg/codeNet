import socket
from client import clientY

try:
    client = clientY()
    client.connect(("127.0.0.1", 80))
    print(client.get_server_list())
    client.close()
except:
    print("main server error")

s = socket.socket()
ip = input("ip: ")
port = int(input("port: "))
s.connect((ip, port))
print(s.recv(1024).decode())
while True:
    to_send = ""
    line = ""
    while True:
        line = input(">>> ")
        to_send += line + "\n"
        if "	" in line or ":" in line:
            pass
        else:
            break

    if not line:
        continue
    if line == "end":
        break
    
    try:
        s.send(to_send[:-1].encode())
        print(s.recv(5000).decode())
    except:
        s.close()
        break
    
