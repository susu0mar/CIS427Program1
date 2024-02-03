#This is file for all server operatons
import socket

#creating socket object which is ipv4 & uses TCP
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 2323))
s.listen()

#this loop runs until a connection is established
while True:
    clientsocket, address = s.accept()
    print(f"Connection Successfully Established")#message to check if connection worked
    #sending string to client
    message_test = "Hello World! "
    clientsocket.send(message_test.encode())

    #close connection
    clientsocket.close()