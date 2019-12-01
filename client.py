import socket

port = 10000
serverAddress = ('localhost', port)
s = socket.socket()
s.connect(serverAddress)
s.sendall(b'mama mia')
input()
s.close()