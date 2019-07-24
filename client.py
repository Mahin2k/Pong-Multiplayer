import socket
  
#creates socket object
s = socket.socket()          
port = 5555                
  
# connects to the server on local computer 
s.connect(('127.0.0.1', port)) 
  
# receive data from the server 
print(s.recv(1024))
# close the connection 
s.close()