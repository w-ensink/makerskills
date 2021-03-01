
import socket
import protocol
import logging

PORT = 50_000
SERVER = socket.gethostbyname('192.168.178.10')
ADDRESS = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


class ClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.protocol = protocol.Protocol()

    def __del__(self):
        self.connection.close()

    def wait_for_message(self):
        length = self.connection.recv(self.protocol.get_header_size()).decode(FORMAT)
        if length:
            length = int(length)
            message = self.connection.recv(length).decode(FORMAT)
            return message

    def send_message(self, message):
        message = self.protocol.encode_text(message)
        length = self.protocol.encode_message_length_header(len(message))
        print(f'message: {message}, length: {length}')
        self.connection.send(length)
        self.connection.send(message)


def wait_for_two_client_connections() -> [ClientConnection, ClientConnection]:
    server.listen()
    client_connections = []
    while len(client_connections) < 3:
        connection, address = server.accept()
        client_connections.append(ClientConnection(connection, address))
        print('client connection made')
    print(f'{len(client_connections)} len client connections')
    return client_connections


class Player:
    def __init__(self, client_connection: ClientConnection):
        self.client_connection = client_connection


if __name__ == '__main__':
    connections = wait_for_two_client_connections()
    player_1 = Player(connections[0])
    player_2 = Player(connections[1])

    msg = player_2.client_connection.wait_for_message()
    print(f'player 1: {msg}')
    player_2.client_connection.send_message('hello from server')
    _ = input('press enter to exit...')
