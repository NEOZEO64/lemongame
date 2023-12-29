import socket
 
# next create a socket object 
s = socket.socket()
print ("Socket successfully created")
 

port = 7127
s.bind(('', port))
 
# put the socket into listening mode 
s.listen(5)
print("socket is listening")
 
while True:
    c, addr = s.accept() # Establish connection with client. 

    c.send('Thank you for connecting'.encode())  # send a thank you message to the client. encoding to send byte type. 
    c.close()

    print('Got connection from', addr )
    break