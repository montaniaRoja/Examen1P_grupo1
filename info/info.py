"""
--METODO CONSULTA--
TRAMA DE ENTRADA: 0100001001 
METODO CONSULTA: 01
CODIGO CLIENTE: 00001001

--METODO PAGO--
TRAMA DE ENTRADA: 02 00001001 01 20230110 00020000
METODO PAGO: 02
CODIGO CLIENTE: 00001001
CUOTA: 01
FECHA: 20230110
MONTO: 00020000

TRAMA DE SALIDA: 00 XBLN-001
EXITOSO: 00  //  01 ERROR
REFERENCIA DE BASE DE DATOS: XBLN-001


--METODO DE REVERSION--
TRAMA DE ENTRADA: 03 00001001 XBLN-001
METODO REVERSION: 03
CODIGO CLIENTE: 00001001 
REFERENCIA: XBLN-001

TRAMA DE SALIDA: 00 EXITOSO //  01 ERROR

    eLIMINA LA FECHADE PAGO REALIZADO Y EL ESTADO VUELVE A (A)


-- INTERFAZ DE TKINTER PARA LAS SIGUIENTES OPERACIOES --
* CONSULTAR UN CLIENTE (PANTALLA)
* PAGAR UNA CUOTA DE UN CLIENTE SIN QUE SE SALTEN LAS CUOTAS PENDIENTES
* REVERSIÓN  




"""

consulta = "0100001001"
pago = "0200001001012023011000020000"
reversion = "0300001001XBLN-001"


data = pago
trama = data[0:2]


if trama == "01":
    print("Consulta cliente")

    codigoCliente = data[2:]
    print(codigoCliente)


elif trama == "02":
    print("Metodo pago")

    cliente = data[2:10]
    print(cliente) 
    
    cuota = data[10:12]
    print(cuota)

    fecha = data[12:20]
    print(fecha)

    monto = data[20:]
    print(monto)

elif trama == "03":
    print("Reversion")



