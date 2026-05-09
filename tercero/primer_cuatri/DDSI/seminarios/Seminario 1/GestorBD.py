import pyodbc

#Clase destinada a la conexión con la base datos y sus operaciones
class GestorDB:
    def __init__(self, driver, host, server_name, port, user, password):
        self.driver = driver
        self.host = host
        self.server_name = server_name
        self.port = port
        self.UID = user
        self.PWD = password
        self.conn = None
        self.cursor = None
#------------------------------------------------------------------------------------
#                                   Conexión
# -----------------------------------------------------------------------------------
    def connect(self):
        try:
            conecction_string = f'Driver={self.driver}; DBQ={self.host}:{self.port}/{self.server_name}; UID={self.UID}; PWD={self.PWD}'
            self.conn = pyodbc.connect(conecction_string)
            self.cursor = self.conn.cursor()
            print ("Conexión exitosa con la base de datos")
        except:
            print("Error al conectar con la base de datos")

    def close(self):
        if not (self.cursor.close):
            self.cursor.close()
            print("Cursor cerrado")
        if not (self.conn.closed):
            self.conn.close()
            print("Conexión cerrada")

# ------------------------------------------------------------------------------------
#                         Transacciones y cambios
# -----------------------------------------------------------------------------------
    def Confirmar(self):
        self.conn.commit()
    def SavePoint(self, nombre):
        self.cursor.execute(f'SAVEPOINT {nombre}')

    def VolverCheckpoint(self,nombre):
        self.cursor.execute(f'ROLLBACK TO SAVEPOINT {nombre}')
    def CancelarTransaccion(self):
        self.cursor.execute("ROLLBACK")

# ------------------------------------------------------------------------------------
#                          Creación y borrado de tablas
# -----------------------------------------------------------------------------------
    def CrearTablas(self):
        self.cursor.execute("""
            CREATE TABLE Stock (
                Cproducto INT PRIMARY KEY,
                Cantidad INT CHECK (Cantidad >= 0)
            );
        """)
        self.cursor.execute("""
            CREATE TABLE Pedido (
                Cpedido INT PRIMARY KEY,
                Ccliente INT,
                Fecha_pedido DATE
            );
        """)
        self.cursor.execute("""
            CREATE TABLE Detalle_Pedido (
                Cpedido INT,
                Cproducto INT,
                Cantidad INT,
                CONSTRAINT Cpedido_clave_externa FOREIGN KEY (Cpedido) REFERENCES Pedido(Cpedido),
                CONSTRAINT Cproducto_clave_externa FOREIGN KEY (Cproducto) REFERENCES Stock(Cproducto),
                CONSTRAINT clave_primaria_Detalle_Pedido PRIMARY KEY (Cpedido, Cproducto)
            );
        """)
        self.conn.commit()
        print("Tablas creadas")

        productos = [
            (1, 0),  # Producto 1, cantidad 100
            (2, 150),  # Producto 2, cantidad 150
            (3, 200),  # Producto 3, cantidad 200
            (4, 250),  # Producto 4, cantidad 250
            (5, 300),  # Producto 5, cantidad 300
            (6, 350),  # Producto 6, cantidad 350
            (7, 400),  # Producto 7, cantidad 400
            (8, 450),  # Producto 8, cantidad 450
            (9, 500),  # Producto 9, cantidad 500
            (10, 550)  # Producto 10, cantidad 550
        ]
        self.cursor.executemany("""INSERT INTO Stock (Cproducto, cantidad) VALUES (?, ?)""", productos)
        self.conn.commit()
    def BorrarTablas(self):
        borrar = ["Detalle_Pedido", "Pedido", "Stock"]
        for tabla in borrar:
            self.cursor.execute(f'DROP TABLE {tabla}')
        print("Tablas borradas")
        self.conn.commit()

# ------------------------------------------------------------------------------------
#                                  Getters
# -----------------------------------------------------------------------------------
    # -------Tablas--------
    def ObtenerTabla(self,tabla):
        self.cursor.execute(f"SELECT * FROM {tabla}")
        return self.cursor.fetchall()

    def NombresTabla(self, tabla):
        self.cursor.execute(f" SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = ? AND OWNER = ?", tabla, self.UID.upper())
        return self.cursor.fetchall()

    def NumElementosTabla(self, tabla):
        return self.cursor.execute(f"SELECT COUNT(*) FROM {tabla}")

    #-------Filas--------
    def ObtenerUnProducto(self, Cproducto):
        self.cursor.execute("SELECT * FROM Stock WHERE Cproducto = ?", (Cproducto))
        return self.cursor.fetchone()
    def ObtenerUnPedido(self, Cpedido):
        self.cursor.execute("SELECT * FROM Pedido WHERE Cpedido = ?", (Cpedido))
        return self.cursor.fetchone()

    def ObtenerUnDetalle_Pedido(self, Cpedido, Cproducto):
        self.cursor.execute("SELECT * FROM Detalle_Pedido WHERE Cpedido = ? AND Cproducto = ?", (Cpedido, Cproducto))
        return self.cursor.fetchone()

    # ------------------------------------------------------------------------------------
    #                                  Modificar filas
    # -----------------------------------------------------------------------------------
    def Modificar_Stock(self, Cproducto, NuevaCantidad):
        self.cursor.execute("""UPDATE STOCK SET CANTIDAD = ? WHERE Cproducto = ?""", (NuevaCantidad, Cproducto))
    # ------------------------------------------------------------------------------------
    #                                  Insertar filas
    # -----------------------------------------------------------------------------------
    def Insertar_Detalle_Pedido(self, Cpedido, Cproducto, Cantidad):
        self.cursor.execute("""INSERT INTO Detalle_Pedido (Cpedido, Cproducto, Cantidad) VALUES (?, ?, ?)""",(Cpedido, Cproducto, Cantidad))
    def Insertar_Stock(self, Cproducto, cantidad):
        self.cursor.execute("""INSERT INTO Stock (Cproducto, cantidad) VALUES (?, ?)""", (Cproducto, cantidad))

    def Insertar_Pedido(self, Cpedido, Ccliente, Fecha_Pedido):
        self.cursor.execute("""INSERT INTO Pedido (Cpedido, Ccliente, Fecha_Pedido) VALUES (?, ?, ?)""",(Cpedido, Ccliente, Fecha_Pedido))
    # ------------------------------------------------------------------------------------
    #                                  Eliminar filas
    # -----------------------------------------------------------------------------------
    def Eliminar_Producto(self, Cproducto):
        self.cursor.execute("""DELETE FROM Stock WHERE Cproducto = ?""", (Cproducto))

    def Eliminar_Pedido(self, Cpedido):
        self.cursor.execute("""DELETE FROM Pedido WHERE Cpedido = ? """,(Cpedido))

    def Eliminar_Detalle_Pedido(self, Cpedido, Cproducto):
        self.cursor.execute("""DELETE FROM Pedido WHERE Cpedido = ? AND Cproducto = ? """,(Cpedido, Cproducto))





