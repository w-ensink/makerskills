
from server import ClientConnection, wait_for_two_client_connections
from game_logic import GameLogic


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

    def start_game(self, face_ids: [str], your_id: str):
        info = '|'.join(face_ids) + '&' + your_id
        self.client_connection.send_message('START' + info)

    def handle_won_game(self):
        self.client_connection.send_message('LOSE')

    def handle_lost_game(self):
        self.client_connection.send_message('LOSE')


if __name__ == '__main__':
    p1, p2 = wait_for_two_client_connections()
    p1, p2 = ClientPlayer(p1), ClientPlayer(p2)

    game = GameLogic()
    game.add_player(p1)
    game.add_player(p2)

    game.setup()
    game.run()
