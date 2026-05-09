#import socket
#s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s_client.sendto(b'Hola clase', ('localhost',12345))
#s_client.close()
import socket

# Crear el socket UDP del cliente
s_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enviar un mensaje al servidor
message = "Hola clase"
s_client.sendto(message.encode(), ('localhost', 12345))

# Esperar la respuesta del servidor
data, serveraddr = s_client.recvfrom(4096)
print("Respuesta del servidor:", data.decode())

# Cerrar el socket
s_client.close()
