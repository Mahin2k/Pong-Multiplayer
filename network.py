import socket
import time


class Network:
    def __init__(self):
        from app import join_ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = join_ip
        print(join_ip)
        self.port = 59555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        print(self.p)

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.sendall(data.encode())
            response =  self.client.recv(2048*2)
            print(response)
            return response
        except socket.error as e:
            print(e)
        except Exception as e:
            print(e)
