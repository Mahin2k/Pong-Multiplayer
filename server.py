import socket
from _thread import *
import sys
from requests import get

currentId = "0"
ip = get('https://api.ipify.org').text
pos = ["0:50,50", "1:100,100"]

def main():
    global ip, currentId, pos
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server = '0.0.0.0'
    port = 59559

    server_ip = socket.gethostbyname(server)
    print("Your IP is: %s" % ip)

    try:
        s.bind((server, port))

    except socket.error as e:
        print(str(e))

    s.listen(2)
    print("Waiting for a connection")



    def threaded_client(conn):
        global currentId, pos
        conn.send(str.encode(currentId))
        currentId = "1"
        reply = ''
        while True:
            try:
                data = conn.recv(2048*2)
                reply = data.decode('utf-8')
                print(reply)
                if not data:
                    conn.send(str.encode("Goodbye"))
                    break
                else:
                    global pos
                    print("Recieved: " + reply)
                    arr = reply.split(":")
                    id = int(arr[0])
                    pos[id] = reply

                    if id == 0: nid = 1
                    if id == 1: nid = 0

                    reply = pos[nid][:]
                    print("Sending: " + reply)
                
                conn.sendall(str.encode(reply))

            except socket.error as e:
                print(e)
                print("couldn't send data")

        print("Connection Closed")
        conn.close()
        sys.exit()

    while True:
        conn, addr = s.accept()
        print("Connected to: ", addr)

        start_new_thread(threaded_client, (conn,))

if __name__ == "__main__":
    main()
    