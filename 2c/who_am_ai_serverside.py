
from server import ClientConnection, Server
from game_logic import GameLogic
import threading


# even though it's called ClientPlayer, it runs on the server
# it resembles a client on the server
#
# sending messages in the following format:
# 'START': start game followed by its picture ID's
# 'QUESTION': when expecting a question
# 'ANSWER': when expecting an answer ('ja' or 'nee')
# 'WIN': to signal this player has won
# 'LOSE': to signal this player has lost
class ClientPlayer(GameLogic.Player):
    def __init__(self, client_connection: ClientConnection):
        self.client_connection = client_connection
        self.score_to_pass_on = ''

    def provide_question(self) -> str:
        self.client_connection.send_message('QUESTION' + self.score_to_pass_on)
        return self.client_connection.wait_for_message()

    def provide_answer(self, question: str) -> str:
        self.client_connection.send_message('ANSWER' + question)
        return self.client_connection.wait_for_message()

    def answer_received(self, answer: str):
        self.client_connection.send_message('RESPONSE' + answer)
        client_response = self.client_connection.wait_for_message()
        if client_response.startswith('OK'):
            self.score_to_pass_on = client_response[2:]

    def start_game(self, serialized_person_data_base: str):
        self.client_connection.send_message('START' + serialized_person_data_base)

    def handle_won_game(self):
        self.client_connection.send_message('WIN')
        print('handle won game')
        # TODO: maybe ask for confirmation from client?
        self.client_connection.close()

    def handle_lost_game(self):
        self.client_connection.send_message('LOSE')
        print('handle lost game')
        # TODO: maybe ask for confirmation from client?
        self.client_connection.close()


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

def main(connection1, connection2):
    p1, p2 = ClientPlayer(connection1), ClientPlayer(connection2)
    game = GameLogic()
    game.add_player(p1)
    game.add_player(p2)
    game.setup()
    game.run()


if __name__ == '__main__':
    PORT = 50_000
    IP_ADDRESS = '192.168.178.10'
    server = Server(ip_address=IP_ADDRESS, port=PORT)

    c1, c2 = server.wait_for_num_client_connections(num=2)
    thread = threading.Thread(target=main, args=(c1, c2))
    thread.start()
    _ = input('press enter to exit')
    server.close()
