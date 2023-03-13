from cryptography.fernet import Fernet
import socket

# Generar una clave de cifrado
clave = Fernet.generate_key()

# Inicializar el objeto Fernet con la clave generada
f = Fernet(clave)

# Crear un socket y conectarse al servidor
s = socket.socket()
host = '172.16.201.232'
port = 8888
s.connect((host, port))

# Enviar la clave al servidor
s.send(clave)

# Esperar a que el servidor esté listo para recibir mensajes
print(s.recv(1024))

while True:
    # Leer el mensaje a enviar
    mensaje = input('Mensaje a enviar: ')

    # Cifrar el mensaje
    mensaje_cifrado = f.encrypt(mensaje.encode())

    # Enviar el mensaje cifrado
    s.send(mensaje_cifrado)

    # Esperar la respuesta del servidor
    respuesta_cifrada = s.recv(1024)

    # Descifrar la respuesta y mostrarla en la consola
    respuesta = f.decrypt(respuesta_cifrada)
    print(f'Servidor: {respuesta.decode()}')