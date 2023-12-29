import socket

s = socket.socket() # Create a socket object 

#s.connect(('127.0.0.1', port)) 
s.connect(('151.217.116.14', 7127)) 
msg = s.recv(1024).decode()  # receive data from the server and decoding to get the string.
s.close()

print(msg)


