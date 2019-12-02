import socket
import time
import sys

# port = 45024
# serverAddress = ('localhost', port)
# s = socket.socket()
# s.connect(serverAddress)
# s.send(b'PUBLISH!@!m12!@!mamao')
# s.recv(1024)
# time.sleep(10)
# s.send(b'PUBLISH!@!m12!@!amerlo')
# s.close()

class Publish():
    def __init__(self, topic, file, time, port = 43024):
        self.port = port
        self.topic = topic
        self.file = file
        self.running = True
        self.time = float(time)

    def run(self):
        serverAddress = ('localhost', self.port)
        self.s = socket.socket()
        self.s.connect(serverAddress)
        print('conectando a servidor')
        with open(self.file) as f:
            for line in f:
                try:
                    msg = 'PUBLISH!@!{0}!@!{1}'.format(self.topic, line)
                    self.s.send(msg.encode())
                    time.sleep(.1)
                    r =  self.s.recv(1024)
                    print(r)
                    time.sleep(self.time)
                except:
                    self.running = False
                    break
        self.s.close()

if __name__ == "__main__":
    if len(sys.argv)<4:
        print('python3 publish.py file tempo topic_name')
        exit()
    s = Publish(topic = sys.argv[3], file = sys.argv[1], time=sys.argv[2])
    s.run()