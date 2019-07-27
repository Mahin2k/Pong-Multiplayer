import socket
import pickle
from requests import get

ip = get('https://api.ipify.org').text


class Network:
    def host(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 59559
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self, *vars):

        for var in vars:
            self.addr = var

        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
