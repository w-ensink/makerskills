from client import ServerConnection
from speech_to_text_input import SpeechToText
import threading
from display import Display
import pygame
from person_data_base import PersonDataBase


PORT = 50_000
IP_ADDRESS = '84.104.226.204'


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------


class WhoAmAIClient(threading.Thread):
    def __init__(self, input_provider, server_connection: ServerConnection, display: Display):
        super().__init__()
        self.server_connection = server_connection
        self.input_provider = input_provider
        self.data_base = None
        self.display = display
        self.keep_running = True

    def stop(self):
        self.keep_running = False

    def run(self):
        while self.keep_running:
            self.handle_next_message()
        self.server_connection.close()

    def handle_start_game(self, message):
        self.data_base = PersonDataBase.from_string(message)
        self.display.set_data_base(self.data_base)
        self.display.set_feedback('Wacht op de andere speler')

    def handle_answer_received(self, answer):
        self.display.set_feedback(f'Het antwoord: "{answer}". Welke personen vallen weg?')
        person_to_remove = self.input_provider.get_user_input()
        # TODO: make mechanism to remove people from display
        self.server_connection.send_message('OK')

    def handle_ask_question(self):
        self.display.set_feedback('Spreek je vraag in')
        question = self.input_provider.get_user_input()
        self.display.set_feedback(f'Ik hoorde: "{question}", wil je dit verzenden?')
        while not self.input_provider.get_user_confirmation():
            self.display.set_feedback('Ik heb het niet verzonden, spreek opnieuw in')
            question = self.input_provider.get_user_input()
            self.display.set_feedback(f'Ik hoorde: "{question}", wil je dit verzenden?')
        self.display.set_feedback('Je vraag is verzonden...')
        self.server_connection.send_message(question)

    def handle_answer_question(self, question):
        self.display.set_feedback(f'Vraag: {question}? Spreek je antwoord in.')
        answer = self.input_provider.get_user_input()
        self.display.set_feedback(f'Ik hoorde: "{answer}", wil je dat versturen?')
        while not self.input_provider.get_user_confirmation():
            self.display.set_feedback('Het bericht is niet verstuurd, spreek opnieuw je antwoord in.')
            answer = self.input_provider.get_user_input()
            self.display.set_feedback(f'Ik hoorde: "{answer}", wil je dat versturen?')
        self.display.set_feedback('Je antwoord is verstuurd.')
        self.server_connection.send_message('RESPONSE' + answer)

    def handle_next_message(self):
        message = self.server_connection.wait_for_message()
        if message.startswith('START'):
            self.handle_start_game(message[5:])

        if message.startswith('QUESTION'):
            self.handle_ask_question()

        if message.startswith('ANSWER'):
            self.handle_answer_question(message[6:])

        if message.startswith('RESPONSE'):
            self.handle_answer_received(message[8:])

        if message.startswith('WIN'):
            self.display.set_feedback('Je hebt gewonnen!')

        if message.startswith('LOSE'):
            self.display.set_feedback('Je hebt verloren, loser.')


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

def main():
    pygame.init()
    clock = pygame.time.Clock()
    display = Display(width=1400, height=1000)
    server_connection = ServerConnection((IP_ADDRESS, PORT))
    input_provider = SpeechToText()
    who_am_ai_client = WhoAmAIClient(input_provider, server_connection, display)
    who_am_ai_client.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                who_am_ai_client.stop()
                return 0

        display.render()
        clock.tick(60)


if __name__ == '__main__':
    exit(main())
