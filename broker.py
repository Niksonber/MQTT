import socket
import selectors
from threading import Thread
import time


class Broker():
    def __init__(self, port = 43024):
        self.nextID = 0
        self.clientsId = {}
        self.topics = {}
        self.topicsLastMsg = {}
        self.selector = selectors.DefaultSelector()
        self.running = 1
        self.port = port
        self.serverAddress = ('localhost', self.port)

    def run(self):
        print('Iniciando servidor {} na porta {}'.format(*self.serverAddress))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(False)
        self.s.bind(self.serverAddress)
        self.s.listen(100)
        self.selector.register(self.s, selectors.EVENT_READ, self.accept)
        while self.running>0:
            try:
                for key, mask in self.selector.select(timeout=1):
                    cb = key.data
                    cb(key.fileobj, mask)
            except:
                break
        print('Desligando Broker')
        self.s.close()
        self.selector.close()

    def accept(self, sock, mask):
        c, addr = sock.accept()
        print('aceitando ({})'.format(addr))
        c.setblocking(False)
        self.selector.register(c, selectors.EVENT_READ, self.read)

    def read(self, socket, mask):
        addr = socket.getpeername()
        print('lendo: ({})'.format(addr))
        msg = socket.recv(1024)
        if msg:
            rsp = ''
            msg = self.prepareMsg(msg)
            code = msg[0]

            if code == 'CONNECT':
                self.clientsId[self.nextID] = (socket, 0.0)
                self.nextID +=1 
                rsp = 'CONNACK'

            elif code == 'DISCONNECT':
                pass
            
            elif code == 'PUBLISH':
                self.running +=1
                self.selector.unregister(socket)
                node, payload = msg[1], msg[2]
                self.topics[node] = []
                rsp = 'PUBACK' + '!@!' + payload
                print('Novo no: {0}'.format(node))
                self.selector.register(socket, selectors.EVENT_READ, self.publish)

            elif code == 'SUBSCRIBE':
                print('Novo inscrito, topico: {0}'.format (msg[1]))
                rsp = self.sub(socket, msg)

            elif code == 'UNSUBSCRIBE':
                print('inscrito removido, topico: {0}'.format (msg[1]))
                rsp = self.unsub(socket, msg)

            socket.send(rsp.encode())
        else:
            print('Fechando')
            self.selector.unregister(socket)
            socket.close()
            #self.running -= 1

    def prepareMsg(self,msg):
        msg = msg.decode()
        msg = msg.split('!@!')
        return msg

    def publish(self, socket, mask):
        addr = socket.getpeername()
        print('pub chegou de: ({})'.format(addr))
        msg = socket.recv(1024)
        if msg:
            msg2 = self.prepareMsg(msg)
            code = msg2[0]
            if code == 'PUBLISH':
                node = msg2[1]
                payload = msg2[2]
                if payload!='':
                    self.topicsLastMsg[node] = payload
                    rsp = 'PUBACK' + '!@!' + payload
                    for client in self.topics[node]:
                        print('encaminhando mensagam para inscrito')
                        print(msg)
                        client.send(msg)
            elif code == 'PINGREQ':
                rsp = 'PINGRESP'
            socket.send(rsp.encode())
        else:
            print('Fechando')
            self.selector.unregister(socket)
            socket.close()
            self.running -= 1


    def sub(self, socket, msg):
        rsp = 'padrao'
        for topic in msg[1:]:
            try:
                self.topics[topic].append(socket)
                rsp = 'SUBACK' + '!@!' + topic
            except:
                #self.running-=1
                break
        return rsp

    def unsub(self, socket, msg):
        rsp = 'padrao'
        for topic in msg[1:]:
            try:
                self.topics[topic].remove(socket)
                rsp = 'UNSUBACK' + '!@!' + topic
            except:
                #self.running-=1
                break
        return rsp



if __name__ == "__main__":        
    b = Broker()
    b.run()