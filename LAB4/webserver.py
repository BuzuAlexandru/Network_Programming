import socket
import signal
import sys
import threading
import json
import re
from time import sleep

# Define the server's IP address and port
HOST = '127.0.0.1'  # IP address to bind to (localhost)
PORT = 8080  # Port to listen on

# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)  # Increased backlog for multiple simultaneous connections
print(f"Server is listening on {HOST}:{PORT}")


# Function to handle client requests
def handle_request(client_socket):
    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    # method = request_line[0]
    path = request_line[1]

    # Initialize the response content and status code
    response_content = ''
    status_code = 200

    f = open('products.json')
    data = json.load(f)

    home = '<h1 align=center vertical-align=center>Homepage!</h1>'
    about = "<p>About us: we're great</p>"
    contact = '<p>Contact here: 06034562456</p>'
    products = '<h1>Product List</h1><br>'

    for i in range(1,len(data)+1):
        products += f'<a href=products/{i}>{data[i-1]["name"]}</a><br><br>'

    # Define a simple routing mechanism
    if path == '/':
        response_content = home
    elif path == '/about':
        response_content = about
    elif path == '/contacts':
        response_content = contact
    elif path == '/products':
        response_content = products
    elif re.search('/products/+\d', path) and int(re.sub('\D', '', path))<=len(data):
        id = int(re.sub('\D', '', path))-1
        response_content = f'''
        
        <h1>{data[id]["name"]}</h1>
        <ul>    
            <li><b>Author: </b><p>{data[id]["author"]}</p></li>
            <li><b>Price: </b><p>{data[id]["price"]}</p></li>
            <li><b>Description: </b><p align=justify>{data[id]["description"]}</p></li>
        </ul>
        '''

    else:
        response_content = '404 Not Found'
        status_code = 404

    # Prepare the HTTP response
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


# Function to handle Ctrl+C and other signals
def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Create a thread to handle the client's request
    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()
