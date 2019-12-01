import socket
import time
port = 41024
serverAddress = ('localhost', port)
s = socket.socket()

s.connect(serverAddress)

s.send(b'SUBSCRIBE!@!m12')
time.sleep(.5)
msg = s.recv(1024)
print(msg)
msg = s.recv(1024)
print(msg)
s.close()
