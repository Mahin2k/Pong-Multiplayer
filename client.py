import socket
  
def join(ip):
    #creates socket object
    s = socket.socket()          
    port = 59555                
    
    # connects to the server on local computer 
    s.connect((ip, port)) 
    
    # receive data from the server 
    print(s.recv(1024))
    # close the connection 
    s.close()