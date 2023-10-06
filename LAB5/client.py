import json
import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12346  # Server's port

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Connect to the server

client_info = {
    'name': '',
    'room': ''
}

client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")


# Function to receive and display messages

def receive_messages():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break  # Exit the loop when the server disconnects

        message = json.loads(message)
        if message['type'] == 'connect_ack':
            print(message["payload"]["message"])

        elif message['type'] == 'notification':
            if message['payload']['room'] == client_info['room']:
                print(message["payload"]["message"])

        elif message['type'] == 'message':
            if message['payload']['room'] == client_info['room']:
                print(f'{message["payload"]["sender"]}: {message["payload"]["text"]}')


# Start the message reception thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True  # Thread will exit when the main program exits
receive_thread.start()

client_info['name'] = input("What is your name: ")
client_info['room'] = input("What room do you want to connect  to: ")

connect_json = {
    'type': 'connect',
    'payload': {
        'name': client_info['name'],
        'room': client_info['room']
    }
}

client_socket.send(json.dumps(connect_json).encode())
print('\nTo exit chat type "exit".')

while True:
    message = input()
    if message.lower() == 'exit':
        break

    msg = {
        "type": "message",
        "payload": {
            "sender": client_info['name'],
            "room": client_info['room'],
            "text": message
        }
    }
    # Send the message to the server
    client_socket.send(json.dumps(msg).encode('utf-8'))

client_socket.close()
