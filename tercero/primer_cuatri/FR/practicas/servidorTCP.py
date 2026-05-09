'''
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 9999))
s.listen(1)
print("Esperando conexión de un cliente...")
sc, addr = s.accept()
print("Cliente conectado desde:", addr)
while True:
    recibido = sc.recv(1024)
    if recibido.decode() == "close":
        print("El cliente ha cerrado la conexión.")
        break
    mensaje_convertido = recibido.decode().lower()
    print(f"{addr[0]} dice:", mensaje_convertido)
    sc.send(mensaje_convertido.encode())
print("Adios.")
sc.close()
s.close()
'''
import socket
import random

# Crear el socket TCP del servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 9999))
s.listen(1)
print("Servidor esperando conexión...")

# Aceptar la conexión del cliente
sc, addr = s.accept()
print("Cliente conectado desde:", addr)

while True:
    # Recibir el mensaje del cliente
    recibido = sc.recv(1024).decode()

    # Finalizar si el cliente envía el mensaje "close"
    if recibido.lower() == "close":
        print("El cliente ha cerrado la conexión.")
        sc.send("Conexión cerrada.".encode())
        break

    # Simular la pérdida del mensaje con un 33% de probabilidad
    if random.random() < 0.33:
        # Notificar al cliente que el mensaje se perdió y necesita reenviarlo
        print("Mensaje perdido. Solicitando reenvío...")
        sc.send("REINTENTAR".encode())
    else:
        # Confirmar la recepción del mensaje
        print(f"Mensaje recibido correctamente: {recibido}")
        sc.send("RECIBIDO".encode())

# Cerrar la conexión
sc.close()
s.close()
