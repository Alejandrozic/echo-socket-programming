"""
    Echo Client

    Developer for CS3622 Fundamentals of Data Communications class project.

    Assignment

    2) Echo Client
        An echo client gets a message from a user and sends the message to the 
        connected reverse echo server. When the reversed message is arrived from 
        the server, it displays the message to the users. If a user wants to stop 
        the client program, the user types “end” to the client. The client sends 
        the message to the reverse echo server, and waits the message “dne” from 
        the server. If the client gets the message “dne”, it terminates itself 
        with displaying “dne” message.
"""

import socket

# DEFINE server IP and Port

HOST = "127.0.0.1" 
PORT = 6000  

# Open a TCP Socket Connection Handler
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to Server
    s.connect((HOST, PORT))
    # Iteratively take user input until the 
    # user has sent the message 'end'.
    while True:
        message: str = input('Message: ')
        message_bytes: bytes = str.encode(message)
        s.sendall(message_bytes)
        data: bytes = s.recv(1024)
        data_str: str = data.decode('utf8')
        print(f"Received {data_str}")
        if data_str == 'dne':
            # Assignment condition to break when
            # server responds with 'dne'.
            break
