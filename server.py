# first of all import the socket library 
import socket                
  
# next create a socket object 
s = socket.socket()          
print("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 55545

# Next bind to the port 
s.bind(('0.0.0.0', port))         
print("socket binded to %s" %(port))
  
# put the socket into listening mode 
s.listen(5)
print("socket is listening")            


while True: 
   # Establish connection with client. 
   c, addr = s.accept()      
   print('Got connection from', addr )
   
   # send a thank you message to the client.  
   # the b is for byte data type
   c.send(b'Thank you for connecting')

   # Close the connection with the client 
c.close() 