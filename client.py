import socket
import pickle
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = 'localhost'
port = 5555
pos = ['0:20,330','1:20,80']

data = pickle.dumps(pos)

s.connect((host, port))

while 1:
    s.sendall(data)

    try:
        response = s.recv(4096*2)
        print(pickle.loads(response))
    except pickle.PickleError as e:
        print(e)
