# interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox
import client
import ast


def salir(ventana):
    ventana.destroy()


def realizarPago(ventana):
    # 02 00001001 01 20230110 00020000
    cliente = entrada.get()
    montoPago = monto.get()
    fecha = entradaFechaPago.get()
    pagarCuota = cuotaApagar.get()
    ct = cuota.get()
    metodoTransaccion = f"020000{cliente}{ct}{fecha}000{montoPago}00"

    if ct == pagarCuota and fecha != "":

        response = client.client(metodoTransaccion)

        messagebox.showinfo("Información", f"Pago realizado con éxito!")
        messagebox.showinfo("Información", f"Referencia: {response}")
        ventana.destroy()
    else:
        messagebox.showerror("Error", "La cuota ingresada o fecha no es válida!")


def reversion(data, ventana):
    cliente = entrada.get()
    ref = referencia.get()
    fechaRef = entradaFechaReferencia.get()
    datosClientes = data
    #0300001001XBLN-001
    metodoTransaccion = f"030000{cliente}{ref}"

    if fechaRef != "" and ref != "":
        def exists_id(datosClientes, fechaRef):

            for row in datosClientes:
                # Fecha == fecha
                if row[4] == fechaRef:
                    return True
            return False

        if exists_id(datosClientes, fechaRef):

            response = client.client(metodoTransaccion)
            if response == "00":

                messagebox.showinfo("Información", "Reversión realizada con éxito!")
                ventana.destroy()
            else:
                messagebox.showinfo("Información", "Ha ocurrido un error en la transacción, Código error: 01")
        else:
            messagebox.showinfo("Info", "La fecha no coincide!")

    else:
        messagebox.showwarning("Error", "Debe ingresar ambos campos!")


def abrir_ventana1():
    data = arrayClientes.get()
    target_id = entrada.get()

    restored_data = ast.literal_eval(data)

    def exists_id(restored_data, target_id):

        for row in restored_data:

            if row[0] == target_id:
                return True
        return False

    if exists_id(restored_data, target_id):

        ventana = tk.Toplevel()
        ventana.title("Consultar Cliente")
        ventana.geometry("750x450")
        ventana.focus()
        ventana.grab_set()
        cliente = entrada.get()

        label = tk.Label(ventana, text=f"Cliente {cliente}", font=("Arial", 17, "bold"))
        label.pack(pady=10)

        metodoTransaccion = f"010000{cliente}"
        datosClientes = client.client(metodoTransaccion)

        # Crear la tabla
        columns = ("Id", "Cuota", "Monto", "Fecha_pago", "Fecha_pago_realizado", "Estado", "Referencia")
        tree = ttk.Treeview(ventana, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

        # Agregar algunos datos de ejemplo
        datos = datosClientes

        for dato in datos:
            tree.insert('', tk.END, values=dato)

        tree.pack(pady=20)

        btn_ventana2 = tk.Button(ventana, text="Realizar Pago", font=("Arial", 10, "bold"), command=abrir_ventana2)
        btn_ventana2.pack(side='left', expand=True, ipadx=30, ipady=20)

        btn_reversion = tk.Button(ventana, text="Reversión", font=("Arial", 10, "bold"),
                                  command=lambda: [abrir_ventana3(datosClientes)])
        btn_reversion.pack(side='left', expand=True, ipadx=30, ipady=20)

        btn_ventana3 = tk.Button(ventana, text="Cancelar", font=("Arial", 10, "bold"), command=lambda: [salir(ventana)])
        btn_ventana3.pack(side='left', expand=True, ipadx=30, ipady=20)
    else:
        messagebox.showerror(f"Error", "El Id ingresado no existe!")


def abrir_ventana2():
    ventana = tk.Toplevel()
    ventana.title("Realizar Pago cliente")
    ventana.geometry("750x400")
    ventana.focus()
    ventana.grab_set()

    cliente = entrada.get()

    label = tk.Label(ventana, text=f"Realizar Pago del Cliente {cliente}", font=("Arial", 17, "bold"))
    label.pack(pady=10)

    # 02 00001001 01 20230110 00020000
    metodoTransaccion = f"040000{cliente}"
    datosClientes = client.client(metodoTransaccion)

    # Crear la tabla
    columns = ("Id", "Cuota", "Monto", "Fecha_pago", "Fecha_pago_realizado", "Estado", "Referencia")
    tree = ttk.Treeview(ventana, columns=columns, show="headings", height=3)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    tree.insert('', tk.END, values=datosClientes[0])

    tree.pack(pady=20)

    global cuotaApagar
    cuotaApagar = tk.StringVar()
    cuotaApagar.set(datosClientes[0][1])

    label_Fechapago = tk.Label(ventana, text="Cuota Número: ", font=("Arial", 12, "bold"))
    label_Fechapago.pack()

    cuotaN = datosClientes[0][1]
    global cuota
    cuota = tk.StringVar()
    txt_cuota = tk.Entry(ventana, textvariable=cuota, width=20, font=("Arial", 14), foreground="#ffac01",
                         justify="center")
    txt_cuota.insert(0, cuotaN)
    txt_cuota.pack()

    global monto
    monto = tk.StringVar()
    monto.set(datosClientes[0][2])

    # Label y Text
    label_Fechapago = tk.Label(ventana, text="Fecha en que realiza el pago: ", font=("Arial", 12, "bold"))
    label_Fechapago.pack()
    label_formato = tk.Label(ventana, text="Año-Mes-Dia (0000-00-00)", font=("Arial", 10))
    label_formato.pack()

    global entradaFechaPago
    entradaFechaPago = tk.StringVar()
    txt_idCliente = tk.Entry(ventana, textvariable=entradaFechaPago, width=20, font=("Arial", 14), foreground="#ffac01",
                             justify="center")
    txt_idCliente.pack()

    btn_pago = tk.Button(ventana, text="Realizar Pago", font=("Arial", 10, "bold"),
                         command=lambda: [realizarPago(ventana)])
    btn_pago.pack(side='left', expand=True, ipadx=30, ipady=20)

    btn_ventana3 = tk.Button(ventana, text="Cancelar", font=("Arial", 10, "bold"), command=lambda: [salir(ventana)])
    btn_ventana3.pack(side='left', expand=True, ipadx=30, ipady=20)


def abrir_ventana3(datosClientes):
    ventana = tk.Toplevel()
    ventana.title("Reversión")
    ventana.geometry("700x400")
    ventana.focus()
    ventana.grab_set()

    cliente = entrada.get()

    label = tk.Label(ventana, text=f"Reversión cliente {cliente}", font=("Arial", 17, "bold"))
    label.pack(pady=10)

    data = datosClientes

    label_Referencia = tk.Label(ventana, text="Referencia: ", font=("Arial", 12, "bold"))
    label_Referencia.pack()

    global referencia
    referencia = tk.StringVar()
    txt_referencia = tk.Entry(ventana, textvariable=referencia, width=20, font=("Arial", 14), foreground="#ffac01",
                              justify="center")
    txt_referencia.pack()

    # Label y Text
    label_FechaReferencia = tk.Label(ventana, text="Fecha de Reversión: ", font=("Arial", 12, "bold"))
    label_FechaReferencia.pack()
    label_formato = tk.Label(ventana, text="Año-Mes-Dia (0000-00-00)", font=("Arial", 10))
    label_formato.pack()

    global entradaFechaReferencia
    entradaFechaReferencia = tk.StringVar()
    txt_FechaReferencia = tk.Entry(ventana, textvariable=entradaFechaReferencia, width=20, font=("Arial", 14),
                                   foreground="#ffac01", justify="center")
    txt_FechaReferencia.pack()

    btn_reversion = tk.Button(ventana, text="Aplicar Reversión", font=("Arial", 10, "bold"),
                              command=lambda: [reversion(data, ventana)])
    btn_reversion.pack(side='left', expand=True, ipadx=30, ipady=20)

    btn_ventana3 = tk.Button(ventana, text="Cancelar", font=("Arial", 10, "bold"), command=lambda: [salir(ventana)])
    btn_ventana3.pack(side='left', expand=True, ipadx=30, ipady=20)


# Ventana Principal
def crear_ventana():
    root = tk.Tk()
    root.title("Pantalla Principal")
    root.geometry("750x550")

    label = tk.Label(root, text="Clientes", font=("Arial", 20, "bold"))
    label.pack(pady=20)

    def cargarDatos(tree):
        metodoTransaccion = "0000001001"
        datosClientes = client.client(metodoTransaccion)

        for item in tree.get_children():
            tree.delete(item)

        for dato in datosClientes:
            tree.insert('', tk.END, values=dato)
        return datosClientes

    # Crear la tabla
    columns = ("Id", "Cuota", "Monto", "Fecha_pago", "Fecha_pago_realizado", "Estado", "Referencia")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    datosClientes = cargarDatos(tree)

    tree.pack(pady=20)

    btn_actualizar = tk.Button(root, text="Actualizar Datos", font=("Arial", 10, "bold"),
                               command=lambda: [cargarDatos(tree)])
    btn_actualizar.pack(pady=5, ipadx=30, ipady=10, )

    # Label y Text
    label_idCliente = tk.Label(root, text="Id del cliente: ", font=("Arial", 12, "bold"))
    label_idCliente.pack()

    global entrada
    entrada = tk.StringVar()
    txt_idCliente = tk.Entry(root, textvariable=entrada, width=20, font=("Arial", 14), foreground="#ffac01",
                             justify="center")
    txt_idCliente.pack()

    global arrayClientes
    arrayClientes = tk.StringVar()
    arrayClientes.set(str(datosClientes))

    # Crear los botones
    btn_ventana1 = tk.Button(root, text="Consultar Cliente", font=("Arial", 10, "bold"), command=abrir_ventana1)
    btn_ventana1.pack(pady=10, ipadx=30, ipady=20, )

    root.mainloop()


if __name__ == "__main__":
    crear_ventana()
