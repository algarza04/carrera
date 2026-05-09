#import socket
#s_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s_server.bind(('',12345))
#data, clientaddr = s_server.recvfrom(4096)
#print("Mensaje recibido:", data.decode())
#s_server.close()


import socket

# Crear el socket UDP del servidor
s_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Vincular el socket al puerto 12345
s_server.bind(('', 12345))

# Recibir el mensaje del cliente
print("Esperando mensaje del cliente...")
data, clientaddr = s_server.recvfrom(4096)

# Imprimir el contenido del mensaje recibido
print("Mensaje recibido del cliente:", data.decode())

# Responder al cliente
response = "Bienvenido a clase"
s_server.sendto(response.encode(), clientaddr)

# Cerrar el socket
s_server.close()
