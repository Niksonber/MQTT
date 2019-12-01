import socket
from threading import Thread
import time


class Broker():
    def __init__(self):
        self.nextID = 0
        self.clientsId = {}
        self.topics = {}
        self.topicsLastMsg = {}

    def publish(self, msg):
        code = msg[0]
        print('publish')
        print(msg)
        rsp = 'padrao'
        if code == 'PUBLISH':
            node = msg[1]
            payload = msg[2]
            self.topicsLastMsg[node] = payload
            rsp = 'PUBACK' + '!@!' + payload
            for client in self.topics[node]:
                print(client)
                client.send(payload.encode())
        elif code == 'PINGREQ':
            rsp = 'PINGRESP'
        return rsp


    def pub(self, socket, addr, msg):
        node = msg[1]
        self.topics[node] = []
        rsp = self.publish(msg)
        print(rsp)
        socket.send(rsp.encode())
        while True:
            try:
                msg = socket.recv(1024)
                msg = msg.decode()
                msg = msg.split('!@!')
                rsp = self.publish(msg)
                print(rsp)
                socket.send(rsp.encode())
                time.sleep(.1)
            except:
                break

    def sub(self, socket, addr, msg):
        rsp = 'padrao'
        for topic in msg[1:]:
            try:
                self.topics[topic].append(socket)
                rsp = 'SUBACK' + '!@!' + topic
            except:
                break
        print(rsp)
        return rsp

    def handle(self, socket, addr):
        print('handlw')
        msg = socket.recv(1024)
        msg = msg.decode()
        msg = msg.split('!@!')
        code = msg[0]
        if code == 'CONNECT':
            self.clientsId[self.nextID] = (socket,addr, 0.0)
            self.nextID +=1 
            rsp = 'CONNACK'
        
        elif code == 'DISCONNECT':
            pass
            # self.clientsId 

        elif code == 'PUBLISH':
            #cria no de comunicação
            x = Thread(target=self.pub, args=(socket,addr, msg))
            x.start()
        elif code == 'SUBSCRIBE':
            self.sub(socket, addr, msg)



def bla(socket, addr):
    while True:
        msg = socket.recv(1024)
        print(addr)
        print(msg)
    socket.close()



if __name__ == "__main__":        
    port = 4102
    s = socket.socket() 

    serverAddress = ('localhost', port)
    s.bind(serverAddress)
    b = Broker()
    t = time.time()
    while True:
        try:
            s.listen(1)
            c, addr = s.accept() 
            b.handle(c,addr)
        except:
            break
    s.close()