import socket
import time

port = 4102
serverAddress = ('localhost', port)
s = socket.socket()

s.connect(serverAddress)
s.send(b'PUBLISH!@!m12!@!mamao')
s.recv(1024)
time.sleep(10)
s.send(b'PUBLISH!@!m12!@!amerlo')
s.close()