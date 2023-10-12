import base64
import os
import socket
import threading
import json

# Server configuration
HOST = '127.0.0.1'  # Loopback address for localhost
PORT = 12346  # Port to listen on

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

media_dir = './SERVER_MEDIA'

print(f"Server is listening on {HOST}:{PORT}")


def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    while True:
        message = client_socket.recv(100_000).decode('utf-8')
        if not message:
            break  # Exit the loop when the client disconnects
        message = json.loads(message)
        print(f"Received from {client_address}: {message['type']}")
        if message['type'] == 'connect':
            ack = {
                "type": "connect_ack",
                "payload": {
                    "message": f"Connected to room {message['payload']['room']}."
                }
            }
            client_socket.send(json.dumps(ack).encode())

            notification = {
                "type": "notification",
                "payload": {
                    "room": message['payload']['room'],
                    "message": f'{message["payload"]["name"]} has joined the room.'
                }
            }
            for client in clients:
                if client != client_socket:
                    client.send(json.dumps(notification).encode('utf-8'))

        elif message['type'] == 'message':
            for client in clients:
                if client != client_socket:
                    client.send(json.dumps(message).encode('utf-8'))

        elif message['type'] == 'download':
            file = message["payload"]["f_name"]
            if not os.path.isfile(media_dir + file):
                print(media_dir + file)
                error = {
                    "type": "res",
                    "payload": {
                        "message": f"File {file} does not exist on the server."
                    }
                }
                client_socket.send(json.dumps(error).encode())
                continue

            content = ''
            file_type = ''

            if file.endswith('.txt'):
                with open(media_dir + file, 'r') as f:
                    content = f.read()
                    file_type = 'txt'
            else:
                with open(media_dir + file, 'rb') as f:
                    content = f.read()
                    content = base64.b64encode(content).decode()
                    file_type = 'img'

            msg = {
                "type": "upload",
                "payload": {
                    "f_name": file,
                    "f_type": file_type,
                    "content": content
                }
            }
            client_socket.send(json.dumps(msg).encode())
            notif = {
                "type": "res",
                "payload": {
                    "message": f"File downloaded successfully."
                }
            }
            client_socket.send(json.dumps(notif).encode())

        elif message['type'] == 'upload':
            if message['payload']['f_type'] == 'txt':
                with open(media_dir+message['payload']['f_name'], 'w') as f:
                    f.write(message['payload']['content'])
            else:
                data = base64.b64decode(message['payload']['content'])
                with open(media_dir+message['payload']['f_name'], 'wb') as f:
                    f.write(data)

            notif = {
                "type": "res",
                "payload": {
                    "message": f"File uploaded successfully."
                }
            }
            client_socket.send(json.dumps(notif).encode())

    # Remove the client from the list
    clients.remove(client_socket)
    client_socket.close()


clients = []


while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

