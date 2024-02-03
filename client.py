#This file is for all client operations
import socket

#creating socket object
cs= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Chose random port number
cs.connect((socket.gethostname(), 2323))

message = cs.recv(1024).decode() #maximum of 1024 bytes can be recieved 

print(f"Message from server: {message}")

#close connection
cs.close()

