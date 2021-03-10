
import socket
import protocol


PORT = 50_000
SERVER = socket.gethostbyname('192.168.178.10')
ADDRESS = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

num_connections = 0


class ClientConnection:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.protocol = protocol.Protocol()
        global num_connections
        num_connections += 1

    def __del__(self):
        self.connection.close()
        global server, num_connections
        num_connections -= 1
        if num_connections == 0:
            server.close()

    def wait_for_message(self):
        length = self.connection.recv(self.protocol.get_header_size()).decode(FORMAT)
        if length:
            length = int(length)
            message = self.connection.recv(length).decode(FORMAT)
            message = self.protocol.decode_text(message)
            return message

    def send_message(self, message):
        message = self.protocol.encode_text(message)
        length = self.protocol.encode_message_length_header(len(message))
        # print(f'message: {message}, length: {length}')
        self.connection.send(length)
        self.connection.send(message)

    def close(self):
        self.connection.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def wait_for_two_client_connections() -> [ClientConnection, ClientConnection]:
    server.listen()
    client_connections = []
    while len(client_connections) < 2:
        connection, address = server.accept()
        client_connections.append(ClientConnection(connection, address))
        print('client connection made')
    print(f'{len(client_connections)} client connections')
    return client_connections[0], client_connections[1]


if __name__ == '__main__':
    connections = wait_for_two_client_connections()
    with connections[0] as player_1, connections[1] as player_2:
        msg = player_2.wait_for_message()
        print(f'player 1: {msg}')
        player_2.send_message('hello from server')
        _ = input('press enter to exit...')
