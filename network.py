import socket
import pickle
import select

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
        return pickle.loads(self.client.recv(4096*2))
        
    def send_ball_pos(self, data):
        self.client.sendall(pickle.dumps(data))

    def listen(self) :
        obj = pickle.loads(self.client.recv(4096*2))
        ball = obj.split(':')[0]
        if ball == 'ball':
            return obj
        else:
            return