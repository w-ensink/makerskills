
import socket
import protocol


FORMAT = 'utf-8'


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
        print('closed client')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class Server:
    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = socket.gethostbyname(ip_address)
        address = (server, port)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(address)
        self.client_connections = []

    def wait_for_num_client_connections(self, num):
        self.server.listen()
        while len(self.client_connections) < num:
            connection, address = self.server.accept()
            self.client_connections.append(ClientConnection(connection, address))
            print('client connection made')
        print(f'{num} client connections made')
        return self.client_connections

    def close(self):
        for c in self.client_connections:
            c.close()
        self.server.close()
        print('closed server')


if __name__ == '__main__':
    connections = None # wait_for_two_client_connections()
    with connections[0] as player_1, connections[1] as player_2:
        msg = player_2.wait_for_message()
        print(f'player 1: {msg}')
        player_2.send_message('hello from server')
        _ = input('press enter to exit...')
