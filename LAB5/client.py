import base64
import json
import os
import re
import shutil
import socket
import threading

'''
download: img.jpg
download: text.txt

upload: img.jpg
upload: text.txt
'''

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
host, client_id = client_socket.getsockname()

media_dir = f'./MEDIA{client_id}'

print(f"Connected to {HOST}:{PORT}")

# Function to receive and display messages

def receive_messages():
    while True:
        message = client_socket.recv(100_000).decode('utf-8')
        if not message:
            break

        message = json.loads(message)
        msg_type = message['type']
        if msg_type == 'connect_ack' or msg_type == 'res':
            print(message["payload"]["message"])

        elif msg_type == 'notification':
            if message['payload']['room'] == client_info['room']:
                print(message["payload"]["message"])

        elif msg_type == 'message':
            if message['payload']['room'] == client_info['room']:
                print(f'{message["payload"]["sender"]}: {message["payload"]["text"]}')

        elif msg_type == 'upload':
            if message['payload']['f_type'] == 'txt':
                with open(media_dir+message['payload']['f_name'], 'w') as f:
                    f.write(message['payload']['content'])
            else:
                data = base64.b64decode(message['payload']['content'])
                with open(media_dir+message['payload']['f_name'], 'wb') as f:
                    f.write(data)


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

os.mkdir(media_dir)

while True:
    message = input()
    msg = dict()
    if message.lower() == 'exit':
        break
    elif re.search('upload: .*', message):
        file = '/'+message[8:]
        if not os.path.isfile(media_dir+file):
            print(f'File {file} does not exist')
            continue

        content = ''
        file_type = ''

        if file[:4] == '.txt':
            with open(media_dir+file, 'r') as f:
                content = f.read()
                file_type = 'txt'
        else:
            with open(media_dir+file, 'rb') as f:
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

    elif re.search('download: .*', message):
        file = message[10:]
        msg = {
            "type": "download",
            "payload": {
                "f_name": f'/{file}',
            }
        }

    else:
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

shutil.rmtree(media_dir)
client_socket.close()
