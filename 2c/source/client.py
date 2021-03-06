
import socket
import sys
import protocol

PORT = 50_000
IP_ADDRESS = '84.104.226.204'
ADDRESS = (IP_ADDRESS, PORT)
FORMAT = 'utf-8'
HEADER = 64


class ServerConnection:
    def __init__(self, address):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(address)
        self.protocol = protocol.Protocol()

    def close(self):
        self.client.close()

    def send_message(self, message):
        encoded_msg = self.protocol.encode_text(message)
        length = self.protocol.encode_message_length_header(len(encoded_msg))
        self.client.send(length)
        self.client.send(encoded_msg)

    def wait_for_message(self):
        length = self.client.recv(self.protocol.get_header_size()).decode(FORMAT)
        if length:
            length = int(length)
            message = self.client.recv(length).decode(FORMAT)
            message = self.protocol.decode_text(message)
            return message


if __name__ == '__main__':
    server_connection = ServerConnection(ADDRESS)
    server_connection.send_message(f'hello from client "{sys.argv[0]}"')
    msg = server_connection.wait_for_message()
    print(f'client received: "{msg}"')
