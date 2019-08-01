import socket
import pickle 
import threading
import sys


HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 5555        # Port to listen on (non-privileged ports are > 1023)

s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

s.listen(2)
print('Server started. Waiting for connection... ')


client_id = 0
pos = ["0:20, 330", "1:1210,330"]


def client_thread(conn):
    global client_id, pos
    conn.send(pickle.dumps(client_id))
    reply = ''
    while 1:
        try:
            data = conn.recv(4096*2)
            reply = str(pickle.loads(data))
            if not data:
                print('Bye')
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print("Sending: " + reply)

            conn.sendall(pickle.dumps(reply))

        
        except:
            pass
    conn.close()
    print('Connection Closed.')

while 1:
    conn, addr = s.accept()
    print('connected to:', addr)
    thread = threading.Thread(target = client_thread, args= (conn,))
    thread.start()
    client_id += 1