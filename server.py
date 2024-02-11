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
# ALREADY DONE WITH INITIAL DATA, KEEP IT COMMENTED OUT (DATA SAVES IN DB AFTER RUN TIME) 

#Adding initial data to db
#cursor = conn.cursor()

# Insert initial data for users
#cursor.executescript("""
#INSERT INTO users (email, first_name, last_name, user_name, password, usd_balance) VALUES
#('john.doe@example.com', 'John', 'Doe', 'johndoe', 'password123', 1000.00),
#('jane.smith@example.com', 'Jane', 'Smith', 'janesmith', 'password123', 1500.00);
#""")

#insert initial data for stocks
#cursor.executescript("""
#INSERT INTO stocks (stock_symbol, stock_name, stock_balance, user_id) VALUES
#('AAPL', 'Apple Inc.', 10, 1),
#('GOOGL', 'Alphabet Inc.', 5, 2),
#('MSFT', 'Microsoft Corp.', 8, 1),
#('TSLA', 'Tesla Inc.', 3, 2);
#""")

#conn.commit()
#print("Initial data added successfully")



#TODO: Need to Figure out how to add to database based on different client commands

    
#Souad
def buy_command(conn, command):
    _, stock_symbol, stock_amount, price_per_stock, user_id= command.split()

    #converting strings into float or int
    stock_amount = float(stock_amount)
    price_per_stock = float(price_per_stock)
    user_id = int(user_id)

    cursor = conn.cursor()

    #check to see if user exists in db
    cursor.execute("SELECT usd_balance FROM users WHERE ID = ?", (user_id,))
    result = cursor.fetchone()

    #if user isn't in db
    if result is None:
        return "Error: User Does Not Exist!!"
    
    usd_balance = result[0]
    total_price = stock_amount *price_per_stock

    #check if user has enough balance
    if usd_balance <total_price:
        return "Error: Not Enough Balance!!"
    
    #Deduct price from user balance
    new_usd_balance = usd_balance - total_price
    #update the table 
    cursor.execute("UPDATE users SET usd_balance = ? WHERE ID = ?", (new_usd_balance, user_id))

    #grab data from the stock table
    cursor.execute("SELECT stock_balance FROM stocks WHERE user_id = ? AND stock_symbol = ?", (user_id, stock_symbol))
    stock_result = cursor.fetchone()

    if stock_result: #if the user already owns some of this stock
        new_stock_balance = stock_result[0] +stock_amount
        #update table 
        cursor.execute("UPDATE stocks SET stock_balance = ? WHERE user_id = ? AND stock_symbol = ?", (new_stock_balance, user_id, stock_symbol))
    
    else: #user doesnt own any of this stock previously
        cursor.execute("INSERT INTO stocks (stock_symbol, stock_name, stock_balance, user_id) VALUES (?, ?, ?, ?)", (stock_symbol, stock_symbol, stock_amount, user_id))


    #Commit all changes to the Database!
    conn.commit()

    return f"200 OK\nBOUGHT: New balance: {new_stock_balance} {stock_symbol}. USD balance ${new_usd_balance}"


#Brooklyn
def sell_command(comm, stock_sym, stock_amo, prc, id):
    data = "200 OK\n" + command + " " + stock_sym + " " + stock_amo + "\ " + price + " " + user_id + "\n"
    print ("testing git")
    return (data)

#Souad
def list_command(comm):
    data = "200 OK\n" + comm + "\n"
    return (data)

#Brooklyn
def balance_command(comm):
    data = "200 OK\n" + comm + "\n"
    return (data)

#Souad
def shutdown_command(comm):
    data = "200 OK\n" + comm + "\n"
    return (data)

#Brooklyn
def quit_command(comm):
    data = "200 OK\n"
    return (data)



#creating socket object which is ipv4 & uses TCP
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 2323))
s.listen()


#defining method to recieve data from client

def recv_all(sock, delimiter = '/n'):
    #have empty list to hold all chunks of data
    data = []


    #read data from socket
    while True:
        #recieve data in chunks
        chunk =sock.recv(4096).decode('utf-8')

        #check if delimiter is in the chunk
        if delimiter in chunk:
            data.append(chunk)
            break #exit loop once delimiter is done
        elif not chunk:
            #if empty, then assume connection is closed
            break
        else:
            #no delimiter encountered, keep gathering chunks
            data.append(chunk)
        
        #Join all chunks into a string and remove delimiter
        return ''.join(data).rstrip(delimiter)


#this loop runs until a connection is established
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} Successfully Established")#message to check if connection worked
    #sending string to client
    message_welcome = "Welcome to this Stock Trading Program\n"
    clientsocket.send(message_welcome.encode())
    
    #Receive a command from the client
    client_message = recv_all(clientsocket)
    print(f"Received command from client: {client_message}")
   	 
    if client_message.startswith("BUY"):
        response = buy_command(conn, client_message)
    #TODO:Need to add for the other commands!!!!!    
    else:
        response = "Error: Invalid command."
   	 

    # Send the response to the client
    clientsocket.sendall(response.encode())
    #close connection
    clientsocket.close()