import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 5555
        self.id = self.connect()

    def connect(self):
        self.client.connect((self.host, self.port))
        return pickle.loads(self.client.recv(4096*2))

    def send(self, data):
        self.client.sendall(pickle.dumps(data)) 
        response = pickle.loads(self.client.recv(4096*2))
        return response
