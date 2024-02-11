#This is file for all server operatons
import socket
#Use sqlite3 library to create simple db for stocks
import sqlite3

#IF DB doesn't work, worst case just use .txt files instead


# Connect to SQLite database
with sqlite3.connect('stock_trading_system.db') as conn:
    cursor = conn.cursor() #create a cursor object to execute SQL commands

    # Create users table (from professors example)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,  
            email VARCHAR(255) NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            user_name VARCHAR(255) NOT NULL,
            password VARCHAR(255),
            usd_balance DOUBLE NOT NULL
        )
    ''')

     # Create stocks table (From professors example)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            stock_symbol VARCHAR(4) NOT NULL,
            stock_name VARCHAR(20) NOT NULL,
            stock_balance DOUBLE,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (ID)
        )
    ''')

    conn.commit()
#
#TODO: Need to Figure out how to add to database based on different client commands
#also need to add initial data (like have 1 or 2 initial users and some stocks)


#creating socket object which is ipv4 & uses TCP
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 2323))
s.listen()

#this loop runs until a connection is established
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} Successfully Established")#message to check if connection worked
    #sending string to client
    message_test = "Welcome to this Stock Trading Program\n"
    clientsocket.send(message_test.encode())

    #close connection
    clientsocket.close()