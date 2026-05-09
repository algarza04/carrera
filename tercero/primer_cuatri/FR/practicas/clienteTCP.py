'''
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9999))
while True:
    mensaje = input("Mensaje a enviar >> ")
    s.send(mensaje.encode())
    if mensaje == "close":  
        break
    respuesta = s.recv(1024)
    print("Respuesta del servidor:", respuesta.decode)
print("Adios.")
s.close()
'''
import socket

# Crear el socket TCP del cliente
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
s.connect(("localhost", 9999))
print("Conectado al servidor.")

while True:
    # Leer el mensaje a enviar
    mensaje = input("Mensaje a enviar (o 'close' para salir) >> ")
    s.send(mensaje.encode())  # Enviar el mensaje al servidor

    # Finalizar si el mensaje es "close"
    if mensaje.lower() == "close":
        print("Cerrando conexión.")
        break

    # Esperar la respuesta del servidor
    while True:
        respuesta = s.recv(1024).decode()
        if respuesta == "REINTENTAR":
            print("Servidor pidió reintento. Reenviando mensaje...")
            s.send(mensaje.encode())  # Reenviar el mismo mensaje
        elif respuesta == "RECIBIDO":
            print("Mensaje recibido correctamente por el servidor.")
            break

# Cerrar el socket
s.close()
