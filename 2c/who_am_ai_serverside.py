
from server import ClientConnection, wait_for_two_client_connections
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

    def provide_question(self) -> str:
        self.client_connection.send_message('QUESTION')
        return self.client_connection.wait_for_message()

    def provide_answer(self, question: str) -> str:
        self.client_connection.send_message('ANSWER' + question)
        return self.client_connection.wait_for_message()

    def answer_received(self, answer: str):
        self.client_connection.send_message('RESPONSE' + answer)
        if self.client_connection.wait_for_message() == 'OK':
            return

    def start_game(self, serialized_person_data_base: str):
        self.client_connection.send_message('START' + serialized_person_data_base)

    def handle_won_game(self):
        self.client_connection.send_message('LOSE')

    def handle_lost_game(self):
        self.client_connection.send_message('LOSE')


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
    c1, c2 = wait_for_two_client_connections()
    thread = threading.Thread(target=main, args=(c1, c2))
    thread.start()
    _ = input('press enter to exit')
    c1.close()
    c2.close()
