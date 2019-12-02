import socket
import time
import sys


# topics = 'm12'
# port = 45024
# serverAddress = ('localhost', port)
# s = socket.socket()

# s.connect(serverAddress)

# s.send(b'SUBSCRIBE!@!m12' + topics)
# time.sleep(.5)
# msg = s.recv(1024)
# print(msg)
# msg = s.recv(1024)      
# print(msg)
# s.close()

class Subscriber():
    def __init__(self, topics, port = 45024):
        self.port = port
        self.topics = ''
        for indx, topic in enumerate(topics):
            self.topics = self.topics + topic
            if indx != len(topics)-1:
                self.topics = self.topics + '!@!'
        self.topics = self.topics.encode()

    def run(self):
        serverAddress = ('localhost', self.port)
        self.s = socket.socket()
        self.s.connect(serverAddress)
        self.s.send(b'SUBSCRIBE!@!m12' + self.topics)
        while True:
            try:
                msg = self.s.recv(1024)
                print(msg)
            except:
                print('deseja encerrar alguma inscrição')
                r = input('1- Sim, 2 -Não')
                if r == '1':
                    r = input('Qual')
                    self.s.send(b'UNSUBSCRIBE!@!m12' + r.encode())
                    continue
                else:
                    print('encerrando')
            break
        self.s.close()

if __name__ == "__main__":
    if len(sys.argv)<2:
        print('tenha certeza que digitou, python3 subscriber.py topicos_separados_por_espaço')
        exit()
    s = Subscriber(topics = sys.argv[1:])
    s.run()