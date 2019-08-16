import socket


class Network:
    def __init__(self, username, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ip
        self.MAX_LENGTH = 4096
        self.port = port
        self.address = (self.host, self.port)
        self.id = ''
        self.state = ''
        self.connect(username)

    def connect(self, username):
        self.client.connect(self.address)
        self.snd(username)
        data = self.rcv(self.MAX_LENGTH)
        if data == 'wait':
            self.state = 'wait'
        elif ':' in data:
            arr = data.split(':')
            print(arr)
            self.state = arr[1]
            self.id = arr[0]

    def snd(self, data):
        self.client.send(data.encode())

    def rcv(self, size):
        return self.client.recv(size).decode()





