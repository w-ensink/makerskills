
import socket
import threading


HEADER = 64
FORMAT = 'utf-8'
PORT = 50_000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(connection, address):
    print(f'New connection: {address}')
    is_connected = True
    while is_connected:
        message_length = connection.recv(HEADER).decode(FORMAT)
        if message_length:
            message_length = int(message_length)
            message = connection.recv(message_length).decode(FORMAT)
            print(f'received: {message}')


def start():
    server.listen()
    while True:
        connection, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, address))
        client_thread.start()
        print(f'There are now {threading.active_count() - 1} clients')


if __name__ == '__main__':
    start()
