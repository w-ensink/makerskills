from client import ServerConnection

PORT = 50_000
IP_ADDRESS = '84.104.226.204'
ADDRESS = (IP_ADDRESS, PORT)




if __name__ == '__main__':
    server_connection = ServerConnection(ADDRESS)

    message = server_connection.wait_for_message()

    if message.startswith('START'):
        print('starting game')
