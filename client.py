import socket
import json

def client(metodoTransaccion) :
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5566
    ADDR = (IP, PORT)
    SIZE = 1024
    FORMAT = "utf-8"
    DISCONNECT_MSG = "!DISCONNECT"


    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f" [CONNECTED] Client connected to server at {IP}: {PORT}")

    connected = True
    while connected:
        msg = metodoTransaccion

        client.send(msg.encode(FORMAT))
        if msg == DISCONNECT_MSG:
            connected = False
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            result = json.loads(msg)
            return result
           
            
         


