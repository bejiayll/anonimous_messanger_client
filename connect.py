import socket
 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
client_socket.connect(('localhost', 12345))

client_socket.send(b'Hello, World')

client_send = ""

while client_send != "EXIT":
    client_send = input()
    client_socket.send(b''+bytes(client_send, encoding="utf-8"))

client_socket.close()