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
pos = None

def client_thread(conn):
    global client_id, pos
    while 1:
        try:
            data = conn.recv(4096*2)
            
            if not data:
                print('Bye')
                break
            else:
                client_id
                reply = pickle.loads(data)
                print(reply)

        
        except socket.error as e:
            print(e)
        except Exception as e:
            print(e)
    conn.close()
    print('Connection Closed.')
    sys.exit()

while 1:
    conn, addr = s.accept()
    client_id = client_id + 1
    print('connected to:', addr)
    thread = threading.Thread(target = client_thread, args= (conn,))
    print("You are player", client_id)
    thread.start()