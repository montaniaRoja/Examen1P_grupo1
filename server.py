import socket
import threading
import connection
import json
import generar

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "SALIR"

def consultas(msg, trama, connDB):

    print("Consulta: ",msg)
    if trama == "00":
        print("Consulta todos")
         
        clientes = connDB.consultarClientes()
        return clientes
    
    elif trama == "01":

        print("Consulta cliente")
        # 0100001001

        codigoCliente = msg[6:]
         
        clientes = connDB.consultarCliente(codigoCliente)
        return clientes

    elif trama == "02":
        
        print("Metodo pago")
        # 0200001001012023-01-1000020000
               
        codigoCliente = msg[6:10]
        cuota = msg[10:12]
        fecha = msg[12:22]
        referencia = generar.generate_serie(1)
       
        respuesta = connDB.pagoCliente(fecha,referencia,codigoCliente, cuota)
        print(referencia)
        return referencia
           
    elif trama == "03":

        print("Reversion")

        #0300001001XBLN-001
        codigoCliente = msg[6:10]
        referencia = msg[10:]
        print(codigoCliente)
        print(referencia)
        respuesta = connDB.reversion(codigoCliente,referencia)
        return respuesta
    
    elif trama == "04":
        print("Consulta cliente por estado A")
         
        codigoCliente = msg[6:]
        respuesta = connDB.consultarClienteEstado(codigoCliente)
        return respuesta
    


def handle_client(conn, addr, connDB) :
    print(f" [NEW CONNECTION] {addr} connected.")
    
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        trama = msg[0:2]

        respuesta = consultas(msg, trama, connDB)
        
        jsonRes = json.dumps(respuesta)
               
        if msg == DISCONNECT_MSG:
            connected = False
        
        #imprime el msg del cliente
        print(f" [{addr}] {msg}")
        msg = f"Msg received: {msg}"

        #Envio respuesta del servidor 
        conn.send(jsonRes.encode(FORMAT))
    
    conn.close()

def main ():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    connDB = connection.Conexion()
    
    print(f"[LISTENING] Server is listening on {IP} : {PORT}")


    while True:
        conn, addr = server.accept ()
        thread = threading.Thread(target=handle_client, args=(conn, addr, connDB))
        thread.start()
        print(f" [CONEXIÓN ESTABLECIDA] {threading.active_count() - 1} ")

if __name__ == "__main__":
    main ()
