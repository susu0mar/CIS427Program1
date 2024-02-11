#This file is for all client operations
import socket

#creating socket object
cs= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Chose random port number
cs.connect((socket.gethostname(), 2323))

message = input("enter command: ") #gets command

cs.send(message.encode()) #send command back to server


data = cs.recv(1024).decode() #maximum of 1024 bytes can be recieved


print(f"Message from server: {data}")


#read input again and give ok

#close connection
cs.close()

