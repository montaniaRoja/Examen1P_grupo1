import sqlite3


class Conexion():
    nombreBD = "manejoClientes.db"

    def __init__(self):
        self.conexion = sqlite3.connect(self.nombreBD, check_same_thread=False)
        self.cursor = self.conexion.cursor()
        print(f"Conected to '{self.nombreBD}' dataBase")

    def cerrar_conexion(self):
        # Cerrar conexión y cursor
        self.cursor.close()
        self.conexion.close()
        print("Conexión cerrada.")

    def crear_tabla(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clientes
                           (id_cliente TEXT NOT NULL,
                            cuota TEXT NOT NULL,
                            monto TEXT NOT NULL,
                            fecha_pago DATE NOT NULL,
                            pagofecharealizado DATE,
                            estado TEXT NOT NULL,
                            referencia TEXT)''')
        print("Tabla 'clientes' creada correctamente.")

    def insertarCliente(self, id, cuota, monto, fecha_pago, pagofecharealizado, estado, referencia):
        self.cursor.execute('''INSERT INTO clientes (id_cliente, cuota, monto, fecha_pago, pagofecharealizado, estado, referencia) 
VALUES 
 (?, ?, ?, ?, ?, ?, ?)''', (id, cuota, monto, fecha_pago, pagofecharealizado, estado, referencia))
        self.conexion.commit()
        print("Cliente registrado")

    def consultarClientes(self):
        self.cursor.execute('''SELECT * FROM clientes''')
        self.conexion.commit()
        clientes = self.cursor.fetchall()
        return clientes

    def consultarCliente(self, id_cliente):
        self.cursor.execute('''SELECT * FROM clientes WHERE id_cliente = ? ''', (id_cliente,))
        self.conexion.commit()
        clientes = self.cursor.fetchall()
        return clientes

    def consultarClienteEstado(self, id_cliente):
        self.cursor.execute('''SELECT * FROM clientes WHERE id_cliente = ? AND estado = "A" ''', (id_cliente,))
        self.conexion.commit()
        cliente = self.cursor.fetchall()
        return cliente

    def pagoCliente(self, fechaPagoRealizado, referencia, id_cliente, cuota):
        self.cursor.execute(
            '''UPDATE clientes SET pagofecharealizado = ?, estado = "B" , referencia = ?  WHERE id_cliente = ? AND cuota = ? ''',
            (fechaPagoRealizado, referencia, id_cliente, cuota,))
        self.conexion.commit()
        return referencia

    def reversion(self, codigoCliente, referencia):
        self.cursor.execute(
            '''UPDATE clientes SET pagofecharealizado = "", estado = "A" , referencia = ""  WHERE id_cliente = ? AND referencia = ? ''',
            (codigoCliente, referencia))
        self.conexion.commit()
        return "00"
