import socket
import select
from requests import get

def main():

    ip = get('https://api.ipify.org/?format=text').text


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # host and port
    host = '0.0.0.0'
    port = 59559

    # binding socket and listening
    sock.bind((host, port))
    sock.listen(2)

    print(f'\n[+] Server started on {ip}:{port}')

    sockets_list = [sock]
    outputs = []
    clients = {}
    users = []

    def get_user(c):
        try:
            return c.recv(1024).decode()

        except Exception as e:
            print(e)

    while True:
        print('\nWaiting for next event')

        #   selecting readable/writable lists with select module
        readable, writable, errs = select.select(sockets_list, outputs, [])

        if readable:
            for i, s in enumerate(readable):
                # check if socket is server socket
                if s == sock:
                    connection, address = sock.accept()
                    sockets_list.append(connection)

                    username = get_user(connection)

                    clients[connection] = username
                    users.append(username)

                    
                    # Closing connection with 3 or more players
                    if len(users) > 2:
                        connection.close()

                    # check if two players are connected
                    elif len(users) == 2:
                        for client, username in clients.items():
                            # sending player id and start signal to all sockets
                            # other than the server socket
                            if client != s:
                                for j, user in enumerate(users):
                                    if clients[client] == user:
                                        client.send(f'{j}:start'.encode())
                                        # print(f'Sending start signal to {user} ID:{j}')
                    else:
                        connection.send('wait'.encode())
                                        


                else:
                    data = s.recv(1024).decode()

                    if not data:
                        s.close()
                        sockets_list.remove(s)
                        del clients[s]

                    elif ':' in data:
                        arr = data.split(':')
                        player_id = 0
                        player_one_pos = arr[0]
                        ball_pos = arr[1]

                        # print('Client one data:', player_one_pos, ball_pos)
                        for j, client in enumerate(clients):
                            if j != player_id:
                                client.send(data.encode())
                                print(f'Sending {data} to player: {j}')
                    elif ':' not in data:
                        if data != 'enemy' or 'player':
                            arr = data.split('.')
                            player_id = 1
                            player_two_pos = arr[0]
                            # print("Client two data:", player_two_pos)
                            for j, client in enumerate(clients):
                                if j != player_id:
                                    client.send(data.encode())
                                    print(f'Sending {data} to player: {j}')


if __name__ == '__main__':
    main()
